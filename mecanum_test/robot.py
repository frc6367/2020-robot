import wpilib
import ctre
import math
from drivetrain import Drivetrain
from intake import Intake
from pneumatic import Pneumatic
from magicbot import MagicRobot


class MyRobot(MagicRobot):
    drivetrain: Drivetrain
    intake: Intake
    pneumatic: Pneumatic

    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(3) # 
        self.drive_l2 = ctre.WPI_VictorSPX(4) #
        self.drive_r1 = ctre.WPI_VictorSPX(1) #
        self.drive_r2 = ctre.WPI_VictorSPX(2) #

        self.solenoid = wpilib.DoubleSolenoid(0,1)

        self.intake_motor = ctre.WPI_TalonSRX(5)
        self.intake_motor.setNeutralMode(self.intake_motor.NeutralMode.Brake)

        self.TWIST_DEAD_BAND = .3

    def teleopInit(self):
        wpilib.LiveWindow.setEnabled(False)

    def testInit(self):
        wpilib.LiveWindow.setEnabled(True)
        

    def teleopPeriodic(self):
        # Victor 1 Doesn't work
        # Victor 2 and 3 don't work moving forward
        # Victor 4 works fine
        # self.driveCartesian()
        # self.intakeButtons()
        self.pneumaticButtons()

    def intakeButtons(self):
        if self.joystick.getRawButton(1):
            self.intake.ballIn()
        elif self.joystick.getRawButton(2):
            self.intake.ballOut()
    
    def pneumaticButtons(self):
        if self.joystick.getRawButton(5):
            self.pneumatic.extend()
        elif self.joystick.getRawButton(3):
            self.pneumatic.retract()

    def drivePolar(self):
        angle = math.tan(self.joystick.getY()/self.joystick.getX())
        angle = math.degrees(angle)
        mag = math.sqrt(self.joystick.getX()**2 + self.joystick.getY()**2)
        self.drivetrain.driveP(mag,math.degrees(angle) - 180)

    def driveCartesian(self):
        t = 0
        if(t > self.TWIST_DEAD_BAND):
            t = self.joystick.getTwist()
        self.drivetrain.driveC(self.joystick.getX(),self.joystick.getY(),self.joystick.getTwist())

# Don't mess with this (Runs Program)
if __name__ == "__main__":
    wpilib.run(MyRobot)