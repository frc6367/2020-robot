#!/usr/bin/env python3
#
# Requires the latest version of pyfrc!
#

import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    """Main robot class"""

    def robotInit(self):
        """Robot-wide initialization code should go here"""

        self.stick = wpilib.Joystick(0)

        # TODO: change to correct motors
        self.intake_motor = wpilib.PWMTalonSRX(1)
        self.belt_motor = wpilib.PWMSparkMax(2)

        self.ball_sensor1 = wpilib.AnalogInput(1)
        self.ball_sensor2 = wpilib.AnalogInput(2)
        self.ball_sensor3 = wpilib.AnalogInput(3)

    def teleopPeriodic(self):

        # Inputs are just for testing purposes to validate the sim, modify
        # this with real control code instead
        self.intake_motor.set(self.stick.getRawAxis(0))
        self.belt_motor.set(self.stick.getRawAxis(2))


if __name__ == "__main__":
    wpilib.run(MyRobot)
