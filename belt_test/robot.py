import wpilib
import rev
import ctre

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.spark = rev.CANSparkMax(5,rev.CANSparkMax.MotorType.kBrushless)
        self.talon = ctre.TalonSRX(6)
        self.speed = 0

    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1)/2
            self.spark.set(-self.speed)
        elif self.joystick.getRawButton(2):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1)/2
            self.talon.set(ctre.ControlMode.PercentOutput,-self.speed)
        else:
            self.speed = 0
            self.spark.set(self.speed)
            self.talon.set(ctre.ControlMode.PercentOutput,self.speed)
        

if __name__ == "__main__":

    wpilib.run(MyRobot)
