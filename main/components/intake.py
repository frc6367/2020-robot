import ctre
import magicbot
class Intake:

    intake_motor: ctre.WPI_TalonSRX

    def setup(self):
        self.speed = 0

    def ballIn(self):
        self.speed = 1
    
    def ballOut(self):
        self.speed = -1
    
    def execute(self):
        self.intake_motor.set(self.speed)
        self.speed = 0