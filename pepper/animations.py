import math


def start_pose(motion): 
    names = ["HipRoll", "HeadPitch", "HeadYaw", "RElbowRoll", "RElbowYaw", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand", "LElbowRoll", "LElbowYaw", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "LHand"]
    angles = [math.radians(0), math.radians(-21.6), math.radians(0.7), math.radians(5.6), math.radians(96.4), math.radians(100.3), math.radians(-5.7), math.radians(-5.7), 0.69, math.radians(-5.9), math.radians(-98.4), math.radians(101.5), math.radians(5.9), math.radians(2.0), 0.69]
    motion.angleInterpolation(names, angles, [1.0]*15, True)


def hello(motion): 
    names = ["HipRoll", "RElbowRoll", "RElbowYaw", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand"]
    angles = [math.radians(9.0), math.radians(74.0), math.radians(119.3), math.radians(27.7), math.radians(-78.3), math.radians(-8.5), 1.0]
    motion.angleInterpolation(names, angles, [1.0]*12, True)
    motion.angleInterpolation("RElbowRoll", math.radians(59.0), 0.5, True)
    motion.angleInterpolation("RElbowRoll", math.radians(74.0), 0.5, True)


def point(motion):
    names = ["RShoulderPitch", "RHand"]
    angles = [math.radians(4.5), 1.0]
    motion.angleInterpolation(names, angles, [1.0]*2, True)


def calm_down(motion): 
    names = ["RElbowRoll", "RElbowYaw", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "RHand", "LElbowRoll", "LElbowYaw", "LShoulderPitch", "LShoulderRoll", "LWristYaw", "LHand"]
    angles_0 = [math.radians(89.5), math.radians(85.3), math.radians(21.8), math.radians(-6.8), math.radians(-59.7), 1.0, math.radians(-78.4), math.radians(-85.9), math.radians(21.2), math.radians(6.1), math.radians(59.5), 1.0]
    motion.angleInterpolation(names, angles_0, [1.0]*12, True)
    
    names_arms = ["RElbowRoll", "RShoulderPitch", "LElbowRoll", "LShoulderPitch"]
    angles_1 = [math.radians(30.2), math.radians(42.7), math.radians(-30.9), math.radians(42.9)]
    angles_2 = [math.radians(89.5), math.radians(21.8), math.radians(-78.4), math.radians(21.2)]

    motion.angleInterpolation(names_arms, angles_1, [1.0]*4, True)
    motion.angleInterpolation(names_arms, angles_2, [1.0]*4, True)
    motion.angleInterpolation(names_arms, angles_1, [1.0]*4, True)

    
def head_no(motion):
    for i in range(2):
        motion.angleInterpolation("HeadYaw", math.radians(35.0), 1.0, True)
        motion.angleInterpolation("HeadYaw", math.radians(-35.0), 1.0, True)
    

def head_yes(motion):
    for i in range(2):
        motion.angleInterpolation("HeadPitch", math.radians(25.0), 1.0, True)
        motion.angleInterpolation("HeadPitch", math.radians(-25.0), 1.0, True)
    
    