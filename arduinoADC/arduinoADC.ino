// Overengineered I2C based ADC using an Arduino NANO.
// It uses 6 Analog Channels (The remaining 2 are needed for the SDA/SCL pins)
// This will send the data of each analog channel as csv.
// The ADC is constantly read and values saved on global variables, then when a request is received, the string is built and sent through I2C
// Each ADC read takes about 0.1ms
// TODO: Use digital inputs for a semaphore indicator?


#include <Wire.h>
#define I2C_ADDRESS 8
#define READ_PERIOD 100 // Analog Read delay cycle, in ms. The actual reading takes a bit longer. Note: each analogread takes about
#define REFVOLTAGE 5.0 //ref voltage so it can be used to map the value
#define ADCCOUNTS 1023 // the value for ADC max number, 2^10 - 1
#define ARRAY_SIZE 12 // Array size in bytes - 6 int is 12 bytes
// NOTE: SDA and SCL are A4, A5.

int adcData[6];

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
  delay(READ_PERIOD); // TODO use millis to decide if value needs to be updated
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void requestEvent() {
  // For now, only "sending the adc data" is required. 
  sendADCdata((byte*) adcData);
}

void sendADCdata(byte *data){
  // function to send de ADC data
  Wire.beginTransmission(I2C_ADDRESS);
    for(int i = 0; i<ARRAY_SIZE; i++){
     Wire.write(data[i]); 
  }
  Wire.endTransmission();
}
