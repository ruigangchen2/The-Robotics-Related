#include <Arduino.h>
#include <Wire.h>
#include "HMC5883L.h"

double HMC5883L::magX, HMC5883L::magY, HMC5883L::magZ = 0;
uint8_t HMC5883L::Data[6] = {0};
int16_t HMC5883L::magPosOff[3] = {0};
int16_t HMC5883L::magNegOff[3] = {0};
double HMC5883L::magGain[3] = {0};
float HMC5883L::magOffset[3] = { (MAG0MAX + MAG0MIN) / 2, (MAG1MAX + MAG1MIN) / 2, (MAG2MAX + MAG2MIN) / 2 };

uint8_t HMC5883L_adrees = 0x1E; // Address of magnetometer

/** Default constructor.
 */
HMC5883L::HMC5883L() {
}

void HMC5883L::getdata(){

  HMC5883L_Read(0x03,HMC5883L::Data,6); // Get magnetometer values
  HMC5883L::magX = ((HMC5883L::Data[0] << 8) | HMC5883L::Data[1]);
  HMC5883L::magZ = ((HMC5883L::Data[2] << 8) | HMC5883L::Data[3]);
  HMC5883L::magY = ((HMC5883L::Data[4] << 8) | HMC5883L::Data[5]);

}

void HMC5883L::calibrate(){
  HMC5883L_Write(0x00, 0x11);
  delay(500); // Wait for sensor to get ready
  getdata(); // Read positive bias values

  HMC5883L::magPosOff[0] = HMC5883L::magX;
  HMC5883L::magPosOff[1] = HMC5883L::magY;
  HMC5883L::magPosOff[2] = HMC5883L::magZ;
  

  HMC5883L_Write(0x00, 0x12);
  delay(500); // Wait for sensor to get ready
  getdata(); // Read positive bias values

  HMC5883L::magNegOff[0] = HMC5883L::magX;
  HMC5883L::magNegOff[1] = HMC5883L::magY;
  HMC5883L::magNegOff[2] = HMC5883L::magZ;

  HMC5883L_Write(0x00, 0x10);// Back to normal
  delay(500); // Wait for sensor to get ready
  
  HMC5883L::magGain[0] = -2500 / float(magNegOff[0] - magPosOff[0]);
  HMC5883L::magGain[1] = -2500 / float(magNegOff[1] - magPosOff[1]);
  HMC5883L::magGain[2] = -2500 / float(magNegOff[2] - magPosOff[2]);
  delay(100); // Wait for sensors to stabilize

}

void HMC5883L::setmode_continuous(){

    HMC5883L_Write(0x02, 0x00);// Configure device for continuous mode

}


/** Write data to the compass by I2C */
void HMC5883L::HMC5883L_Write(uint8_t register_address, uint8_t data)
{
  Wire.beginTransmission(HMC5883L_adrees);
  Wire.write(register_address);
  Wire.write(data);
  Wire.endTransmission();
}

/** Read data from the compass by I2C  
 */
uint8_t HMC5883L::HMC5883L_Read(uint8_t register_address, uint8_t buffer[], uint8_t length)
{
  // Write the register address that we will begin the read from, this
  // has the effect of "seeking" to that register
  Wire.beginTransmission(HMC5883L_adrees);
  Wire.write(register_address);
  Wire.endTransmission();
  
  // Read the data starting at that register we seeked
  Wire.requestFrom(HMC5883L_adrees, length);

  if(Wire.available() == length)
  {
    for(uint8_t i = 0; i < length; i++)
    {
      buffer[i] = Wire.read();
    }
    
    return length;
  }
  return 0;
}