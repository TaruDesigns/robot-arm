# Quick test te see if I2C values make any sense
 
from smbus import SMBus
import time
 
 
def buildInt(higherByte, lowerByte):
    return (higherByte << 8) | lowerByte

addr = 0x50 # device address
bus = SMBus(1) # indicates /dev/ic2-1
number_of_ints = 6 # number of ints to read
dValues = dict() # dictionary to hold the values

print ("Starting")
while True:
    block_status = bus.read_i2c_block_data(addr, 0, 14)
    print(block_status)
    del block_status[0]
    del block_status[-1] # Delete leading and trailing bytes
    print(block_status)
    for i in range(number_of_ints):
        motorname = "Motor " + str(i)
        dValues[motorname] = buildInt(block_status[i*2], block_status[i*2 + 1])
        print(motorname + " " + str(dValues[motorname]))
    time.sleep(2)
    