# Class to read the ARDUINO ADC values through I2C
 
from smbus import SMBus
import time

class ADCino:
    def __init__(self) -> None:
        self.__bus = SMBus(1) # indicates /dev/ic2-1
        self.__addr = 0x50 # device address on 0x50
        self.__number_of_ints = 6 # number of ints to read
        self.chValues = dict() # dictionary to hold the values
    def _getdValues_(self) -> dict:
        """internal, acquire data.

        Returns:
            dict: _description_
        """
        block_status = self.__bus.read_i2c_block_data(self.__addr, 0, 14) # It reads 14 bytes: Leading + (6*2 bytes) of data + Trailing
        del block_status[0]
        del block_status[-1]# Delete leading and trailing bytes, they should be = 200
        for i in range(0, self.__number_of_ints):
            chName = "CH" + str(i)
            #print("ValHigh: " + str(block_status[i*2]) + " ValLow " + str(block_status[i*2 + 1]))
            self.chValues[chName] = self._buildInt(block_status[i*2], block_status[i*2 + 1])
            # CH0, CH1, CH2, CH3, CH4, CH5
    def _buildInt(self, higherByte, lowerByte) -> int:
        """Build integer from two bytes

        Args:
            higherByte (byte): higher byte
            lowerByte (byte): lower byte

        Returns:
            int: full int
        """
        return (higherByte << 8) | lowerByte
    def get_all_data(self) -> dict:
        """Refresh data buffer and return it. If channel name is provided, then return only the value for that channel

        Args:
            none
        Returns:
            dict: Full dict of values
        """
        self._getdValues_()
        return self.chValues

    def get_channel_data(self, channel, refresh=False) -> int: #TODO only request one channel instead of all data
        """Return only the value for that channel. Set bool to true to refresh buffer
        Args:
            channel (str): Channel name (CH0, CH1...)
            refresh (bool): If True, refresh the data buffer
        Returns:
            int: Value of channel
        """
        print(str(channel))
        if refresh:
            self._getdValues_()
        chName = "CH" + str(channel)
        return self.chValues[chName]
 