import wpilib
import ctre
import math
from components.drivetrain import Drivetrain
from components.intake import Intake
# from pneumatic import Pneumatic
from magicbot import MagicRobot

class MyRobot(MagicRobot):
    drivetrain: Drivetrain
    intake: Intake
    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(3) # 
        self.drive_l2 = ctre.WPI_VictorSPX(4) #
        self.drive_r1 = ctre.WPI_VictorSPX(1) #
        self.drive_r2 = ctre.WPI_VictorSPX(2) #

        self.intake_motor = ctre.WPI_TalonSRX(5)
        self.intake_motor.setNeutralMode(self.intake_motor.NeutralMode.Brake)

    # def teleopInit(self):
    #     wpilib.LiveWindow.setEnabled(False)

    # def testInit(self):
    #     wpilib.LiveWindow.setEnabled(True)
        

    def teleopPeriodic(self):
        self.drive()
        self.intakeButtons()

    def intakeButtons(self):
        if self.joystick.getRawButton(1):
            self.intake.ballIn()
        elif self.joystick.getRawButton(2):
            self.intake.ballOut()
    

    def drive(self):
        self.drivetrain.drive(-self.joystick.getY(),self.joystick.getTwist())


# Don't mess with this (Runs Program)
if __name__ == "__main__":
    wpilib.run(MyRobot)