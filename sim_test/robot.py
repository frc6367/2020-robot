#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
import rev

if wpilib.RobotBase.isSimulation():
    is_sim = True
    import physics
    import time
else:
    is_sim = False


class MyRobot(wpilib.TimedRobot):
    """Main robot class"""

    def robotInit(self):
        """Robot-wide initialization code should go here"""
        self.joystick = wpilib.Joystick(0)
        self.spark = rev.CANSparkMax(5,rev.CANSparkMax.MotorType.kBrushless)
        self.talon = ctre.TalonSRX(6)
        self.speed = 0

        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        # self.l_motor = ctre.VictorSPX(1)
        # self.r_motor = ctre.VictorSPX(2)
        # self.l_motor2 = ctre.VictorSPX(3)
        # self.r_motor2 = ctre.VictorSPX(4)

        # Position gets automatically updated as robot moves
        # self.gyro = wpilib.AnalogGyro(1)

        # self.l_motor2.follow(self.l_motor)
        # self.r_motor2.follow(self.r_motor)

        # self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)

        self.motor = wpilib.Jaguar(4)

        self.limit1 = wpilib.DigitalInput(1)
        self.limit2 = wpilib.DigitalInput(2)

        self.sensor1 = wpilib.AnalogInput(0)
        self.position = wpilib.AnalogInput(1)

        self.step = -1

        self.kBallTreshhold = 1.75

        if is_sim:
            self.physics = physics.PhysicsEngine()
            self.last_tm = time.time()

    if is_sim:
        # TODO: this needs to be builtin
        def robotPeriodic(self):
            now = time.time()
            tm_diff = now - self.last_tm
            self.last_tm = now
            self.physics.update_sim(now, tm_diff)

    def autonomousInit(self):
        """Called when autonomous mode is enabled"""

        self.timer = wpilib.Timer()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-1.0, -0.3)
        else:
            self.drive.arcadeDrive(0, 0)

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""
        
        # self.drive.arcadeDrive(self.lstick.getY(), self.lstick.getX())
        #self.drive.arcadeDrive(self.lstick.getRawAxis(1), self.lstick.getRawAxis(3))

        # Move a motor with a Joystick
        y = self.rstick.getY()

        # stop movement backwards when 1 is on
        if self.limit1.get():
            y = max(0, y)

        # stop movement forwards when 2 is on
        if self.limit2.get():
            y = min(0, y)

        self.motor.set(y)

        self.autoIntake()

    def operatedIntake(self):
        if self.joystick.getRawButton(1):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1)/2
            self.talon.set(ctre.ControlMode.PercentOutput,-self.speed)
        elif self.joystick.getRawButton(2):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1)/2
            self.spark.set(-self.speed)
        else:
            self.spark.set(0)
            self.talon.set(ctre.ControlMode.PercentOutput,0)

    def autoIntake(self):
        if self.joystick.getRawButton(1):
            self.step = 0

        if self.joystick.getRawButton(2):
            self.step = -1

        self.speed = self.joystick.getRawAxis(3)
        self.speed = 1 - (self.speed + 1)/2

        if self.step == 0:
            self.talon.set(ctre.ControlMode.PercentOutput,-self.speed)
            if self.ballPresent(self.sensor1):
                if self.ballPresent(self.position):
                    self.step = 2
                else:
                    self.step = 1

        elif self.step == 1:
            self.spark.set(-self.speed)
            self.talon.set(ctre.ControlMode.PercentOutput,0)
            if self.ballPresent(self.position):
                self.step = -1
        
        elif self.step == 2:
            self.talon.set(ctre.ControlMode.PercentOutput,0)
            if not self.ballPresent(self.position):
                self.step = 3

        elif self.step == 3:
            self.spark.set(-self.speed)
            self.talon.set(ctre.ControlMode.PercentOutput,0)
            if self.ballPresent(self.position):
                self.step = -1

        # elif self.step == 2:
        #     self.speed = self.joystick.getRawAxis(3)
        #     self.speed = 1 - (self.speed + 1)/2
        #     self.spark.set(-self.speed)
        #     self.talon.set(ctre.ControlMode.PercentOutput,0)
        #     if not self.ballPresent(self.position):
        #         self.step = -1
        else:
            self.spark.set(0)
            self.talon.set(ctre.ControlMode.PercentOutput,0)
        #     self.speed = self.joystick.getRawAxis(3)
        #     self.speed = 1 - (self.speed + 1)/2
        #     if self.joystick.getRawButton(6):
        #         self.speed *= -1
        #     self.spark.set(-self.speed)
        # elif self.joystick.getRawButton(2):
        #     self.speed = self.joystick.getRawAxis(3)
        #     self.speed = 1 - (self.speed + 1)/2
        #     if self.joystick.getRawButton(6):
        #         self.speed *= -1
        #     self.talon.set(ctre.ControlMode.PercentOutput,-self.speed)
        # else:
        #     self.speed = 0
        #     self.spark.set(self.speed)
        #     self.talon.set(ctre.ControlMode.PercentOutput,self.speed)


    def ballPresent(self, sensor):
        if sensor.getVoltage() > self.kBallTreshhold:
            return True
        return False

if __name__ == "__main__":

    wpilib.run(MyRobot)