# ----------------------------
# LIBRARIES

# External libraries
import time
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685 as Adafruit_PCA9685
# Standard GPIO for the Raspberry
import board
import busio
import digitalio
# import arduino ADC
import ADCino
import pandas
import RobotServo as Servo
# Settings TODO: use json?
from .Settings import *


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# ----------------------------
# PARAMETERS

# ----------------------------
# CODE

class RobotArm:

    # PARAMETERS


    def __init__(self):
        #TODO use Logging library
        print('Initialize PWM board controller')
        # Initialise the PCA9685 using the default address (0x40).
        self.__pwm = Adafruit_PCA9685.PCA9685()

        print('Set frequency')
        # Set the frequency
        self.__pwm.set_pwm_freq(self.SERVO_MOTOR_FREQUENCY)

        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__adc = ADCino.ADCino()

        self.__joints = [] # TODO List comprehension
        for i in range(0, 5):
            print('Initialize joint ' + str(i))
            self.__joints.append(Servo(self.__pwm, \
                                    JOINT_PWM_CHANNELS[i], \
                                    PWM_BOARD_RESOLUTION, \
                                    JOINT_MIN_ANGLE[i], \
                                    JOINT_MAX_ANGLE[i], \
                                    self.__adc, \
                                    JOINT_ADC_INPUT[i], \
                                    pandas.read_csv(self.JOINT_0_ANGLE_ADS_VALUE_MAP_PATH)))
        print('Initialization done')
        
    def move_joint(self, joint:int, angle:int):  
        
        print('Move the servo')
        self.__joints[joint].move(angle)

    def calibrate_servo(self, joint:int):
        print('Calibrate the servo: ' + str(joint))')
        self.__joints[joint].calibrate(JOINT_0_ANGLE_ADS_VALUE_MAP_PATH)

if __name__ == "__main__":
    
    # robot_arm = RobotArm()
    # robot_arm.move()

    Robot = RobotArm
