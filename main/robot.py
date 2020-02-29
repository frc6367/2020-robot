import wpilib
import ctre
import math
import navx
from components.drivetrain import Drivetrain
from components.intake import Intake
from components.overallIntake import Overall
# from pneumatic import Pneumatic
from magicbot import MagicRobot

if wpilib.RobotBase.isSimulation():
    is_sim = True
    import physics
    import time

else:
    is_sim = False

class MyRobot(MagicRobot):
    drivetrain: Drivetrain
    intake: Overall
    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(1) # 
        self.drive_l2 = ctre.WPI_VictorSPX(2) #
        self.drive_r1 = ctre.WPI_VictorSPX(3) #
        self.drive_r2 = ctre.WPI_VictorSPX(4) #

        self.encoder_l = wpilib.Encoder(0,1)
        self.encoder_r = wpilib.Encoder(2,3)

        self.nav = navx.AHRS.create_spi() #Gyros can only be used on channels 0 or 1

        self.intake_motor = ctre.WPI_TalonSRX(5)
        self.intake_motor.setNeutralMode(ctre.NeutralMode.Brake)

        self.shooter_motor = ctre.WPI_TalonSRX(6)
        self.shooter_motor.setNeutralMode(ctre.NeutralMode.Brake)

        if is_sim:
            self.physics = physics.PhysicsEngine()
            self.last_tm = time.time()

    # def teleopInit(self):
    #     wpilib.LiveWindow.setEnabled(False)

    # def testInit(self):
    #     wpilib.LiveWindow.setEnabled(True)

    if is_sim:
        def robotPeriodic(self):
            now = time.time()
            tm_diff = now - self.last_tm
            self.last_tm = now
            self.physics.update_sim(now, tm_diff)


    def teleopPeriodic(self):
        self.drive()
        self.intakeButtons()
        self.shooterButtons()

    def intakeButtons(self):
        if self.joystick.getRawButton(1):
            self.intake.ballIn()

    # def shooterButtons(self):
    #     if self.joystick.getRawButton(3):
    #         self.shooter.shoot()
    

    def drive(self):
        self.drivetrain.drive(-self.joystick.getY(),self.joystick.getTwist())
    

    # Returns A Command
    def getAutonomousCommand(self):
        pass

# Don't mess with this (Runs Program)
if __name__ == "__main__":
    wpilib.run(MyRobot)