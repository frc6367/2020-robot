
import ctre
import wpilib
import wpilib.drive
import wpilib.kinematics
import wpilib.geometry
import navx
import magicbot
import math
class Drivetrain:

    drive_l1: ctre.WPI_VictorSPX
    drive_l2: ctre.WPI_VictorSPX
    drive_r1: ctre.WPI_VictorSPX
    drive_r2: ctre.WPI_VictorSPX

    encoder_l: wpilib.Encoder
    encoder_r: wpilib.Encoder

    nav: navx.AHRS

    def setup(self):
        self.drive_l2.follow(self.drive_l1)
        self.drive_r2.follow(self.drive_r1)
        self.speed = 0
        self.rotation = 0
        self.maxOut = 0
        self.mdrive = wpilib.drive.DifferentialDrive(self.drive_l1,self.drive_r1)

        self.kdistancePulse = 0.1524*math.pi/4 # This has to change to the correct value
        self.kgyroReverse = False

        self.modometry = wpilib.kinematics.DifferentialDriveOdometry(wpilib.geometry.Rotation2d.fromDegrees(self.getHeading()))

        self.encoder_l.reset()
        self.encoder_r.reset()
        self.encoder_l.setDistancePerPulse(self.kdistancePulse)

        self.volts_l = 0
        self.volts_r = 0

        self.auto = True

    def resetDrive(self,pose):
        self.resetEncoders()
        self.modometry.resetPosition(pose)

    def resetEncoders(self):
        self.encoder_l.reset()
        self.encoder_r.reset()

    def resetNavx(self):
        self.nav.reset()

    def getLeftEncoder(self):
        return self.encoder_l.getRaw()

    def getRightEncoder(self):
        return self.encoder_r.getRaw()

    def getPose(self):
        return self.modometry.getPose()

    def getWheelSpeed(self):
        return wpilib.kinematics.DifferentialDriveWheelSpeeds(self.encoder_l.getRate(),self.encoder_r.getRate())

    def getAverageDistance(self):
        return (self.encoder_l.getDistance() + self.encoder_r.getDistance())/2

    def getTurnRate(self):
        if self.kgyroReverse:
            return self.nav.getRate() * -1
        return self.nav.getRate()

    def getHeading(self):
        return math.remainder(self.nav.getAngle(), 360) * (-1.0 if self.kgyroReverse else 1.0)

    # def IEEEremainder(self,dividend,divisor):
    #     return dividend - (divisor * round(dividend / divisor))

    def setMaxOutput(self, value):
        self.maxOut = value


    def drive(self, speed, rotation):
        self.speed = speed
        self.rotation = rotation
        self.auto = False

    def driveVolts(self, volts_l, volts_r):
        self.volts_l = volts_l
        self.volts_r = volts_r
        self.auto = True

    def execute(self):
        if self.auto:
            self.drive_l1.setVoltage(self.volts_l)
            self.drive_r1.setVoltage(-self.volts_r)
            self.mdrive.feed()    
            
        else:        
            self.mdrive.arcadeDrive(self.speed,self.rotation)

        self.modometry.update(
            wpilib.geometry.Rotation2d.fromDegrees(self.getHeading()),
            self.encoder_l.getDistance(),
            self.encoder_r.getDistance()
        )
        self.speed = 0
        self.rotation = 0
        self.volts_l = 0
        self.volts_r = 0