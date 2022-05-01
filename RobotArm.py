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

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# ----------------------------
# PARAMETERS

# ----------------------------
# CODE

class RobotArm:

    # PARAMETERS
    PWM_BOARD_RESOLUTION = 4096 # PWM control board resolution
    SERVO_MOTOR_FREQUENCY = 50 #In Hz
    
    JOINT_0_ANGLE_ADS_VALUE_MAP_PATH = 'data/angle_ads_value_map_joint_0.csv'

    def __init__(self):
        
        print('Initialize PWM board controller')
        # Initialise the PCA9685 using the default address (0x40).
        self.__pwm = Adafruit_PCA9685.PCA9685()

        print('Set frequency')
        # Set the frequency
        self.__pwm.set_pwm_freq(self.SERVO_MOTOR_FREQUENCY)

        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__adc = ADCino.ADCino()
        
        self.__joints = []
        self.__joints.append(Servo(self.__pwm,0,self.PWM_BOARD_RESOLUTION,0,270,self.__adc,0, pandas.read_csv(self.JOINT_0_ANGLE_ADS_VALUE_MAP_PATH)))
        # self.__joints.append(Servo(self.__pwm,1,self.PWM_BOARD_RESOLUTION,0,270,self.__adc,1))
        # self.__joints.append(Servo(self.__pwm,2,self.PWM_BOARD_RESOLUTION,0,270,self.__adc,2))
        # self.__joints.append(Servo(self.__pwm,3,self.PWM_BOARD_RESOLUTION,0,270,self.__adc,3))
        # self.__joints.append(Servo(self.__pwm,4,self.PWM_BOARD_RESOLUTION,0,270,self.__ads2,0))
        # self.__joints.append(Servo(self.__pwm,5,self.PWM_BOARD_RESOLUTION,0,270,self.__ads2,1))

    def move(self):
        
        print('Move the servo')
        self.__joints[0].move(0)
        # self.__joints[1].move(0)
        time.sleep(3)
        
        self.__joints[0].move(180)
        # self.__joints[1].move(90)
        time.sleep(3)
        
        self.__joints[0].move(90)
        # self.__joints[1].move(270)
        time.sleep(3)
        
        self.__joints[0].move(120)
        # self.__joints[1].move(200)
        time.sleep(3)

def calibrate_servos():
    
    PWM_BOARD_RESOLUTION = 4096 # PWM control board resolution
    SERVO_MOTOR_FREQUENCY = 50 #In Hz
    JOINT_0_ANGLE_ADS_VALUE_MAP_PATH = 'data/angle_ads_value_map_joint_0.csv'

    print('Initialize PWM board controller')
    # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    # Set the frequency
    pwm.set_pwm_freq(SERVO_MOTOR_FREQUENCY)

    i2c = busio.I2C(board.SCL, board.SDA)
    adc = ADCino.ADCino

    servo0 = Servo(pwm,0,PWM_BOARD_RESOLUTION,0,270,adc,0, None)

    servo0.calibrate(JOINT_0_ANGLE_ADS_VALUE_MAP_PATH)

if __name__ == "__main__":
    
    # robot_arm = RobotArm()
    # robot_arm.move()

    calibrate_servos()
