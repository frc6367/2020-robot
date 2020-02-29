import wpilib
import ctre
from constants import Constants as c
class Trajectory:

    def getCommand(self):
        autoVoltageConstraint = wpilib.trajectory.constraint.DifferentialDriveVoltageConstraint(
            wpilib.controller.SimpleMotorFeedforward(c.ksVolts,c.kvVoltSecondsPerMeter,c.kaVoltSecondsSquaredPerMeter),
            c.kDriveKinematics,
            10)
        
        config = wpilib.trajectory.TrajectoryConfig(c.kMaxSpeedMetersPerSecond,c.kMaxAccelerationMetersPerSecondSquared).setKinematics(c.kDriveKinematics)
        

