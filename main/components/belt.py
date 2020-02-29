import ctre
import magicbot
class Belt:

    belt_motor: ctre.WPI_TalonSRX
    
    def setup(self):
        self.speed = 0

    def forward(self):
        self.speed = 1

    def backwards(self):
        self.speed = -1

    def execute(self):
        self.belt_motor.set(self.speed)
        self.speed = 0
