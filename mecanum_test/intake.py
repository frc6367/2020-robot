import ctre
import magicbot


class Intake:

    intake_motor: ctre.WPI_TalonSRX

    speed = magicbot.will_reset_to(0)
    magnitude = magicbot.tunable(0.5)

    #TO DO: Find the correct directions for the intake and outake.
    def ballIn(self):
        self.speed = self.magnitude

    def ballOut(self):
        self.speed = -self.magnitude

    def execute(self):
        self.intake_motor.set(self.speed)