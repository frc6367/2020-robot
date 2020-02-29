import ctre
import magicbot
class Intake:

    intake_motor: ctre.WPI_TalonSRX
    
    def setup(self):
        self.speed = 0
        self.min = 0
        self.max = 4
        self.pos = 0
    def changePos(self,position):
        self.pos += position 
        if(self.pos < self.min):
            self.pos=0
        if(self.pos > self.max):
            self.pos=4
        
    def ballIn(self):
        self.speed = 1

    def ballOut(self):
        self.speed = -1
    
    
    def execute(self):
        self.intake_motor.set(self.speed)
        self.speed = 0