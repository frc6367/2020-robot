import ctre
import magicbot


class Intake:

    intake_motor: ctre.WPI_TalonSRX

    speed = magicbot.will_reset_to(0)

    #TO DO: Find the correct directions for the intake and outake.
    def ballIn(self):
        self.speed = 1

    def ballOut(self):
        self.speed = -1

    def execute(self):
        self.intake_motor.set(self.speed)