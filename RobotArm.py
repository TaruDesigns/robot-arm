# ----------------------------
# LIBRARIES

# External libraries
import time
# Import the PCA9685 module.

# Standard GPIO for the Raspberry
import board
import busio
#from adafruit_motor import servo
import Adafruit_PCA9685
import digitalio
# import arduino ADC
import ADCino
from RobotServo import RobotServo
# Settings TODO: use json?
import Settings as stn


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
        #Initialise the I2C bus
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        # Initialise the PCA9685 using the default address (0x40).
        self.__pwm = Adafruit_PCA9685.PCA9685()
        print('Set frequency')
        # Set the frequency
        self.__pwm.set_pwm_freq(stn.SERVO_MOTOR_FREQUENCY)
        
        #Initialize the ADC
        self.__adc = ADCino.ADCino()

        self.__joints = [] # TODO rewrite this as a list comprehension
        for i in range(0, stn.NUMBER_OF_JOINTS):
            print('Initialize joint ' + str(i))
            self.__joints.append(RobotServo(self.__pwm, \
                                    stn.JOINT_PWM_CHANNELS[i], \
                                    stn.PWM_BOARD_RESOLUTION, \
                                    stn.JOINT_MIN_ANGLE[i], \
                                    stn.JOINT_MAX_ANGLE[i], \
                                    self.__adc, \
                                    stn.JOINT_ADC_INPUT[i], \
                                    stn.JOINT_VALUE_MAP_PATH[i]))
        print('Initialization done')

    def move_joint(self, joint:int, angle:int):  
        print('Move the servo')
        self.__joints[joint].move(angle)

    def calibrate_servo(self, joint:int):
        print('Calibrate the servo: ' + str(joint))
        self.__joints[joint].calibrate()
    def show_position(self):
        for joint in self.__joints:
            angle = joint.__evaluate_current_angle()
            print (angle)



if __name__ == "__main__":
    

    Robot = RobotArm()
    print("Check each joint: \n")
    while True:
        command = input("Enter command (move, calibrate, position)\n")
        if command == "move":
            angle = int(input("Enter angle: "))
            joint = int(input("Enter joint: "))
            Robot.move_joint(joint, angle)
        elif command == "calibrate":
            joint = int(input("Enter joint: "))
            Robot.calibrate_servo(joint)
        elif command == "position":
            Robot.show_position()
        else:
            print("Command not recognised")
        time.sleep(1)
