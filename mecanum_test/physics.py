#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#


from pyfrc.physics.drivetrains import MecanumDrivetrain
from pyfrc.physics.units import units


class PhysicsEngine(object):
    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.position = 0

        self.drivetrain = MecanumDrivetrain()


    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """
        try:
            _ = hal_data["CAN"][3]
        except (KeyError, IndexError):
            # talon must not be initialized yet
            return
        # Simulate the drivetrain
        l1_motor = hal_data["CAN"][1]["value"]
        l2_motor = hal_data["CAN"][2]["value"]
        r1_motor = hal_data["CAN"][4]["value"]
        r2_motor = hal_data["CAN"][3]["value"]


        x, y, angle = self.drivetrain.get_vector(l2_motor, r2_motor, l1_motor, r1_motor)
        x *= tm_diff
        y *= tm_diff
        angle *= tm_diff
        self.physics_controller.distance_drive(x, y, angle)

        # Sorta simulate the elevator
        # talon_data = hal_data["CAN"][7]
        # speed = int(4096 * 4 * talon_data["value"] * tm_diff)
        # talon_data["quad_position"] += speed
        # talon_data["quad_velocity"] = speed
