
import ctre
import wpilib.drive
import magicbot

class Drivetrain:

    drive_l1: ctre.WPI_VictorSPX
    drive_l2: ctre.WPI_VictorSPX
    drive_r1: ctre.WPI_VictorSPX
    drive_r2: ctre.WPI_VictorSPX

    def setup(self):
        self.drive_l2.follow(self.drive_l1)
        self.drive_r2.follow(self.drive_r1)
        self.speed = 0
        self.rotation = 0
        self.mdrive = wpilib.drive.DifferentialDrive(self.drive_l1,self.drive_r1)

    def drive(self, speed, rotation):
        self.speed = speed
        self.rotation = rotation

    def execute(self):
        self.mdrive.arcadeDrive(self.speed,self.rotation)