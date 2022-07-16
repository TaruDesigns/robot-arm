// I2C based ADC using Arduino Pro Micro (or any other Arduino with 6 analog channels + the I2C pins)
// It uses 6 Analog Channels (The remaining 2 are needed for the SDA/SCL pins)
// The ADC is constantly read and values saved on global variables, then when a request is received, the string is built and sent through I2C
// Each ADC read takes about 0.1ms
// TODO: Use digital inputs for a semaphore indicator?
// Each "read request" will trigger a write (send) of 14 bytes: One leading byte (200) + trailing byte (200) act as delimiters.
// Ints are sent Big Endian (First Byte is the "higher" byte)


#include <Wire.h>
#define I2C_ADDRESS 80 // 0x50
#define READ_PERIOD 10 // Analog Read delay cycle, in ms.
#define REFVOLTAGE 5.0 //ref voltage so it can be used to map the value. Not used here but good ot keep in mind
#define ADCCOUNTS 1023 // the value for ADC max number, 2^10 - 1. Not used here but good to keep in mind
#define ARRAY_SIZE 6 // Array size in ints = number of analogreads
#define LED_PIN 13 // The Onboard LED Pin
#define LEADING_TRAILING_BYTE_VALUE 200 // The value for the leading and trailing byte.
// NOTE: SDA and SCL are A4, A5.

uint16_t adcData[6]; // Global Buffer

void setup() {
  Wire.begin(I2C_ADDRESS);       // join i2c bus
  Wire.onRequest(requestEvent); // register event
}

void loop() {
  adcData[0] = analogRead(A0);
  adcData[1] = analogRead(A1);
  adcData[2] = analogRead(A2);
  adcData[3] = analogRead(A3);
  adcData[4] = analogRead(A6);
  adcData[5] = analogRead(A7);
  delay(READ_PERIOD); // TODO use millis to decide if value needs to be updated?
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void requestEvent() {
  // For now, only "sending the adc data" is required.
  sendADCdata(adcData);
}

void sendADCdata(uint16_t *data) {
  // function to send ADC data
  Wire.write(LEADING_TRAILING_BYTE_VALUE);
  for (int i = 0; i < ARRAY_SIZE; i++) {
    Wire.write(highByte(data[i]));
    Wire.write(lowByte(data[i]));
  }
  Wire.write(LEADING_TRAILING_BYTE_VALUE);
}
