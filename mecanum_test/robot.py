import wpilib
import ctre
from drivetrain import Drivetrain
from magicbot import MagicRobot

class MyRobot(MagicRobot):
    drivetrain: Drivetrain

    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(0)
        self.drive_l2 = ctre.WPI_VictorSPX(1)
        self.drive_r1 = ctre.WPI_VictorSPX(2)
        self.drive_r2 = ctre.WPI_VictorSPX(3)


    def teleopPeriodic(self):
        self.drivetrain.drive(self.joystick.getX(),self.joystick.getY(),self.joystick.getTwist())

if __name__ == "__main__":
    wpilib.run(MyRobot)