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
    self.yspeed = 0
    self.xspeed = 0
    self.zrotation = 0
    
    #Used to change the variables
  def drive(self, xs, ys, zr):
    self.xspeed = xs
    self.yspeed = ys
    self.zrotation = zr
    #Runs the code
  def execute(self):
    self.mdrive.driveCartesian(self.yspeed,self.xspeed,self.zrotation,0)