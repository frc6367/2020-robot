
import wpilib
import hal

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.ball = hal.SimDevice("ball1")
        self.value = self.ball.createDouble("position", False, 0)
        self.stick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        self.value.set(self.stick.getY())

if __name__ == '__main__':
    wpilib.run(MyRobot)