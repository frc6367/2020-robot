
import wpilib
import hal

import math

import hal.simulation

class MyRobot(wpilib.TimedRobot):

    # 5 balls

    # 3 sensors
    # - position

    # belts/motors
    # - speed

    # tasks
    # - track balls and where they are
    # - is sensor activated?
    # - are balls jammed? defined as 'balls touch each other'

    def robotInit(self):
        self.ball_device = hal.SimDevice("balls")

        self.ball_insert = self.ball_device.createBoolean("insert", False, False)

        self.balls = [self.ball_device.createDouble(str(i), False, float('nan')) for i in range(5)]

        self.sensor1 = wpilib.AnalogInput(1)
        self.sensorSim1 = hal.simulation.AnalogInSim(1)

        self.sensor2 = wpilib.AnalogInput(2)
        self.sensorSim2 = hal.simulation.AnalogInSim(2)

        self.sensor3 = wpilib.AnalogInput(3)
        self.sensorSim3 = hal.simulation.AnalogInSim(3)

        self.intake_motor = wpilib.PWMTalonSRX(1)
        self.intake_motor_sim = hal.simulation.PWMSim(1)

        self.belt_motor = wpilib.PWMTalonSRX(2)
        self.belt_motor_sim = hal.simulation.PWMSim(1)

        self.stick = wpilib.Joystick(0)

        self.last_tm = wpilib.Timer.getFPGATimestamp()

    def robotPeriodic(self):
        now = wpilib.Timer.getFPGATimestamp()
        tm_diff = now - self.last_tm

        # TODO: need a list of balls that are inserted, and balls that are not inserted

        # is ball inserted?
        if self.ball_insert.get():
            # 'insert' a new ball
            print("insert detected")
            self.balls[0].set(0)
            self.ball_insert.set(False)

        # sim code goes here

        # position: velocity*tm_diff
        belt_velocity = self.belt_motor_sim.getSpeed()
        intake_velocity = self.intake_motor_sim.getSpeed()

        # compute where balls are
        # if they overlap with a sensor position, set analog voltage to N
        # otherwise set to 0

        # compute if balls overlap with each other when overlapping the belt motor. If so, raise an exception

        self.sensorSim1.setVoltage(0)


        self.last_tm = now

    def teleopPeriodic(self):
        self.value.set(self.stick.getY())


if __name__ == '__main__':
    wpilib.run(MyRobot)