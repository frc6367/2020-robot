import wpilib
import ctre
import math
import navx
from components.drivetrain import Drivetrain
from components.intake import Intake
from components.shooter import Shooter
# from pneumatic import Pneumatic
from magicbot import MagicRobot

class MyRobot(MagicRobot):
    drivetrain: Drivetrain
    intake: Intake
    shooter: Shooter
    def createObjects(self):

        #Creates the joystick objects
        self.joystick = wpilib.Joystick(0)

        #Creates the motor control objects
        self.drive_l1 = ctre.WPI_VictorSPX(1) # 
        self.drive_l2 = ctre.WPI_VictorSPX(2) #
        self.drive_r1 = ctre.WPI_VictorSPX(3) #
        self.drive_r2 = ctre.WPI_VictorSPX(4) #

        self.encoder_l = wpilib.Encoder(0,1)
        self.encoder_r = wpilib.Encoder(2,3)

        self.nav = navx.AHRS.create_spi() #Gyros can only be used on channels 0 or 1

        self.intake_motor = ctre.WPI_TalonSRX(5)
        self.intake_motor.setNeutralMode(ctre.NeutralMode.Brake)

        self.shooter_motor = ctre.WPI_TalonSRX(6)
        self.shooter_motor.setNeutralMode(ctre.NeutralMode.Brake)

    # def teleopInit(self):
    #     wpilib.LiveWindow.setEnabled(False)

    # def testInit(self):
    #     wpilib.LiveWindow.setEnabled(True)
        

    def teleopPeriodic(self):
        self.drive()
        self.intakeButtons()
        self.shooterButtons()

    def intakeButtons(self):
        if self.joystick.getRawButton(1):
            self.intake.ballIn()
        elif self.joystick.getRawButton(2):
            self.intake.ballOut()

    def shooterButtons(self):
        if self.joystick.getRawButton(3):
            self.shooter.shoot()
    

    def drive(self):
        self.drivetrain.drive(-self.joystick.getY(),self.joystick.getTwist())


# Don't mess with this (Runs Program)
if __name__ == "__main__":
    wpilib.run(MyRobot)