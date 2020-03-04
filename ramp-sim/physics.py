import hal
import hal.simulation


from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import math

BALL_SIZE = 7.0
BALL_SIZE_HALF = BALL_SIZE / 2.0

BALL_DETECT_V = 1.25
BALL_MISSING_V = 2.5


class PhysicsEngine:
    def __init__(self, physics_controller: PhysicsInterface):

        self.physics_controller = physics_controller

        # Ball control
        self.ball_device = hal.SimDevice("Balls")
        self.ball_insert = self.ball_device.createBoolean("insert", False, False)

        # The 'value' of each ball is either 'nan' (not present) or it
        # is the distance the ball lies along the ramp in inches
        self.balls = [
            self.ball_device.createDouble(f"center {i}", False, float("nan"))
            for i in range(5)
        ]

        # Ramp params (adjust these for realism!!)
        self.ramp_params = hal.SimDevice("Ramp Params")

        # Max speed of the motors, sensor positions (all units are in inches)
        self.intake_speed = self.ramp_params.createDouble("intake speed", False, 12)

        # Represents the end of when the intake motor affects the ball's center
        self.intake_pos_end = self.ramp_params.createDouble("intake end pos", False, 18)
        self.belt_speed = self.ramp_params.createDouble("belt speed", False, 12)

        # Represents the start of when the belt affects the ball's center
        self.belt_pos_start = self.ramp_params.createDouble("belt pos start", False, 16)
        self.belt_pos_end = self.ramp_params.createDouble("belt pos end", False, 45)

        self.ball_sensor1_pos = self.ramp_params.createDouble("sensor 1 pos", False, 17)
        self.ball_sensor2_pos = self.ramp_params.createDouble("sensor 2 pos", False, 25)
        self.ball_sensor3_pos = self.ramp_params.createDouble("sensor 3 pos", False, 42)

        # How wide is the detection beam?
        self.sensor_sensitivity = self.ramp_params.createDouble(
            "sensor sens", False, 0.25
        )

        self.intake_motor = hal.simulation.PWMSim(1)
        self.belt_motor = hal.simulation.PWMSim(2)

        # Analog inputs for ball sensors
        # 1 is closest to intake, and so on
        self.ball_sensor1 = hal.simulation.AnalogInSim(1)
        self.ball_sensor2 = hal.simulation.AnalogInSim(2)
        self.ball_sensor3 = hal.simulation.AnalogInSim(3)

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """
        self.ramp_simulation(tm_diff)

    def ramp_simulation(self, tm_diff: float) -> None:
        """
            A simplistic simulation of the interaction between balls and
            motors on our ramp. A more realistic sim would take the physics
            of the motors into account, but this should be a good first
            approximation?
        """

        # Has a ball just been inserted?
        if self.ball_insert.value:
            # 'insert' a new ball by setting its position at the starting point
            for ball in self.balls:
                if math.isnan(ball.value):
                    ball.value = 0
                    print("Ball inserted!")
                    break

            self.ball_insert.value = False

        # Valid balls
        balls = [ball for ball in self.balls if not math.isnan(ball.value)]

        # Initialize sensors
        self.ball_sensor1.setVoltage(BALL_MISSING_V)
        self.ball_sensor2.setVoltage(BALL_MISSING_V)
        self.ball_sensor3.setVoltage(BALL_MISSING_V)

        if not balls:
            return

        # Compute motor movements
        intake_move = self.intake_motor.getSpeed()
        if abs(intake_move) < 0.05:
            intake_move = 0

        belt_move = self.belt_motor.getSpeed()
        if abs(belt_move) < 0.05:
            belt_move = 0

        intake_move = intake_move * self.intake_speed.value * tm_diff
        belt_move = belt_move * self.belt_speed.value * tm_diff

        # Retrieve these values only once for efficiency
        intake_pos_end = self.intake_pos_end.value
        belt_pos_start = self.belt_pos_start.value
        belt_pos_end = self.belt_pos_end.value

        ss = self.sensor_sensitivity.value

        b1_pos = self.ball_sensor1_pos.value
        b1_start, b1_end = (b1_pos - ss, b1_pos + ss)

        b2_pos = self.ball_sensor2_pos.value
        b2_start, b2_end = (b2_pos - ss, b2_pos + ss)

        b3_pos = self.ball_sensor3_pos.value
        b3_start, b3_end = (b3_pos - ss, b3_pos + ss)

        ball_positions = []

        for ball in balls:

            #
            # Compute ball movement
            # - if the center of the ball overlaps the range of the specified motor,
            #   then it is moved using the value computed above
            # - if it overlaps both motors, the movement is additive
            #

            ball_position = ball.value

            if ball_position >= 0 and ball_position <= intake_pos_end:
                ball_position += intake_move
                ball.value = ball_position

            if ball_position >= belt_pos_start and ball_position <= belt_pos_end:
                ball_position += belt_move
                ball.value = ball_position

            #
            # Compute sensor detections
            # - If either edge of the ball lies between the sensors start
            #   or end position, set the voltage appropriately
            #

            ball_start = ball_position - BALL_SIZE_HALF
            ball_end = ball_position + BALL_SIZE_HALF

            if (b1_start >= ball_start and b1_start <= ball_end) or (
                b1_end >= ball_start and b1_end <= ball_end
            ):
                self.ball_sensor1.setVoltage(BALL_DETECT_V)

            if (b2_start >= ball_start and b2_start <= ball_end) or (
                b2_end >= ball_start and b2_end <= ball_end
            ):
                self.ball_sensor2.setVoltage(BALL_DETECT_V)

            if (b3_start >= ball_start and b3_start <= ball_end) or (
                b3_end >= ball_start and b3_end <= ball_end
            ):
                self.ball_sensor3.setVoltage(BALL_DETECT_V)

            # Did the ball leave the ramp?
            if ball_position < 0 or ball_position > belt_pos_end:
                print("Ball removed!")
                ball.value = float("nan")
            else:
                ball_positions.append(ball_position)

        # Finally, determine if any of the balls overlapped each other
        # - Sort by distance to make it easier to compute ball overlap
        ball_positions = sorted(ball_positions)
        for i in range(1, len(ball_positions)):
            if ball_positions[i] - ball_positions[i - 1] < BALL_SIZE:
                print("=" * 72)
                print(" " * 20, "FAIL: balls overlapped!!")
                print(" " * 20, ", ".join("%.3f" % bp for bp in ball_positions))
                print("=" * 72)
                for ball in self.balls:
                    ball.value = float("nan")
                break

