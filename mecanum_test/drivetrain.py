import ctre
import wpilib.drive
import magicbot


class Drivetrain:
  
  #Takes the motor control objects from robot.py
  drive_l1: ctre.WPI_VictorSPX
  drive_l2: ctre.WPI_VictorSPX
  drive_r1: ctre.WPI_VictorSPX
  drive_r2: ctre.WPI_VictorSPX

  #Sets up the rest of the variables that will be determined by the input of the joystick
  def setup(self):
    self.mdrive = wpilib.drive.MecanumDrive(self.drive_l1,self.drive_l2,self.drive_r1,self.drive_r2)
    self.drive_l1.setNeutralMode(self.drive_l1.NeutralMode.Brake)
    self.drive_l2.setNeutralMode(self.drive_l2.NeutralMode.Brake)
    self.drive_r1.setNeutralMode(self.drive_r1.NeutralMode.Brake)
    self.drive_r2.setNeutralMode(self.drive_r2.NeutralMode.Brake)
    self.yspeed = 0
    self.xspeed = 0
    self.zrotation = 0
    self.mag = 0
    self.angle = 0
    self.rot = 0
    
    #Used to change the variables
  def driveC(self, xs, ys, zr):
    self.xspeed = xs**3
    self.yspeed = ys**3
    self.zrotation = zr
 
  def execute(self):
    self.mdrive.driveCartesian(-self.xspeed,-self.yspeed,self.zrotation,0)