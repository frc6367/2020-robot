import wpilib
class Pneumatic:

    solenoid: wpilib.DoubleSolenoid

    def on_enable(self):
        self.current = self.solenoid.Value.kOff

    def extend(self):
        self.current = self.solenoid.Value.kForward

    def retract(self):
        self.current = self.solenoid.Value.kReverse

    def execute(self):
        self.solenoid.set(self.current)