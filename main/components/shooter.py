import ctre
import magicbot
class Shooter:

    shooter_motor: ctre.WPI_TalonSRX
    
    def setup(self):
        self.speed = 0

    def shoot(self):
        self.speed = 1
    
    def execute(self):
        self.shooter_motor.set(self.speed)
        self.speed = 0