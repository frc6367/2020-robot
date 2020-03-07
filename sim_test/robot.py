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
        self.spark = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.talon = ctre.TalonSRX(6)
        self.speed = 0

        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.l_motor = ctre.WPI_VictorSPX(1)
        self.r_motor = ctre.WPI_VictorSPX(4)
        self.l_motor2 = ctre.WPI_VictorSPX(2)
        self.r_motor2 = ctre.WPI_VictorSPX(3)

        # Position gets automatically updated as robot moves
        # self.gyro = wpilib.AnalogGyro(1)

        self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)
        self.drive2 = wpilib.drive.DifferentialDrive(self.l_motor2, self.r_motor2)

        self.sensor1 = wpilib.AnalogInput(0)
        self.sensor2 = wpilib.AnalogInput(1)
        self.sensor3 = wpilib.AnalogInput(2)

        # state (steps/stages) for the intake
        # refer to def operatedIntake(self) about implementation
        self.step = -1

        # value for the sensor that detects if ball is there
        # if the value is above 1.8 the ball is there otherwise it is not
        self.kBallTreshhold = 1.6

        self.kBeltSpeed = -0.3

        # if in simulation mode it turns on the physics engine
        # initializes time

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
        """Called every couple of milseconds"""
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-1.0, -0.3)
        else:
            self.drive.arcadeDrive(0, 0)

    def teleopInit(self):
        self.step = -1
        self.spark.set(0)
        self.talon.set(ctre.ControlMode.PercentOutput, 0)

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""

        # self.drive.arcadeDrive(self.lstick.getY(), self.lstick.getX())
        # self.drive.arcadeDrive(self.lstick.getRawAxis(1), self.lstick.getRawAxis(3))

        # Move a motor with a Joystick

        self.drive.arcadeDrive(
            -self.joystick.getY(), self.joystick.getRawAxis(2), False
        )
        self.drive2.arcadeDrive(
            -self.joystick.getY(), self.joystick.getRawAxis(2), False
        )

        self.autoIntake()

    def operatedIntake(self):
        if self.joystick.getRawButton(1):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1) / 2
            self.talon.set(ctre.ControlMode.PercentOutput, -self.speed)
        elif self.joystick.getRawButton(2):
            self.speed = self.joystick.getRawAxis(3)
            self.speed = 1 - (self.speed + 1) / 2
            self.spark.set(-self.speed)
        else:
            self.spark.set(0)
            self.talon.set(ctre.ControlMode.PercentOutput, 0)

    def autoIntake(self):
        if self.joystick.getRawButton(1):
            self.step = 0

        if self.joystick.getRawButton(2):
            # if not self.ballPresent(self.sensor3):
            self.step = -1
            self.spark.set(0)
            self.talon.set(ctre.ControlMode.PercentOutput, 0)

        if self.joystick.getRawButton(5):
            self.spark.set(-1)
        elif self.step == -1:
            self.spark.set(0)
        # elif self.ballPresent(self.sensor3):
        #     self.step = -1
        #     self.talon.set(ctre.ControlMode.PercentOutput,0)
        #     self.spark.set(0)

        self.speed = self.joystick.getRawAxis(3)
        self.speed = 1 - (self.speed + 1) / 2

        # Steps
        if self.step == 0:
            self.talon.set(ctre.ControlMode.PercentOutput, -self.speed)
            if self.ballPresent(self.sensor1):
                self.step = 1
                self.talon.set(ctre.ControlMode.PercentOutput, 0)

        elif self.step == 1:
            self.spark.set(self.kBeltSpeed)
            if not self.ballPresent(self.sensor1):
                self.step = 2

        elif self.step == 2:
            self.spark.set(self.kBeltSpeed)
            if self.ballPresent(self.sensor2):
                self.step = -1
                self.spark.set(0)
                self.talon.set(ctre.ControlMode.PercentOutput, 0)

    def ballPresent(self, sensor):
        if sensor.getVoltage() > self.kBallTreshhold:
            return True
        return False


if __name__ == "__main__":

    wpilib.run(MyRobot)
