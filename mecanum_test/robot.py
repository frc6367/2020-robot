import wpilib
import ctre
import math
from drivetrain import Drivetrain
from magicbot import MagicRobot

class MyRobot(MagicRobot):
    drivetrain: Drivetrain

    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(3)
        self.drive_l2 = ctre.WPI_VictorSPX(4)
        self.drive_r1 = ctre.WPI_VictorSPX(1)
        self.drive_r2 = ctre.WPI_VictorSPX(2)

        self.TWIST_DEAD_BAND = .3


    def teleopPeriodic(self):
        # Victor 1 Doesn't work
        # Victor 2 and 3 don't work moving forward
        # Victor 4 works fine
        self.driveCartesian()

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
if __name__ == "__main__":
    wpilib.run(MyRobot)