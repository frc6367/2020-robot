import ctre
import wpilib
import magicbot
class Overall:

    # Going to modify later
    belt_motor: ctre.WPI_TalonSRX
    intake_motor: ctre.WPI_TalonSRX

    def setup(self):
        self.kBallTreshhold = 1250 # If a sensor reads a value lower than it there is no ball.

        self.pos1 = False
        self.pos2 = False
        self.full = False

        self.intake_speed = .8
        self.move_speed = .2
        self.shoot_speed = 1

        self.sensor1 = wpilib.AnalogInput(0)
        self.sensor2 = wpilib.AnalogInput(0)
        self.sensor3 = wpilib.AnalogInput(0)

        self.step = -1

    def ballIn(self):
        if self.step < 0:
            self.step = 0


    def ballPresent(self, sensor):
        if sensor.getValue() < self.kBallTreshhold:
            return False
        return True
    
    def stop(self):
        self.step = -1

    def execute(self):
        if self.step == 0:
            self.intake_motor.set(self.intake_speed)
            if self.ballPresent(self.sensor1):
                self.step = 1
        elif self.step == 1:
            self.belt_motor.set(self.move_speed)
            if self.ballPresent(self.sensor2):
                self.step = -1
    



