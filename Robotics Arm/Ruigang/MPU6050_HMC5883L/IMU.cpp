#include "IMU.h"
#include "I2Cdev.h"
#include "HMC5883L.h"
#include <Arduino.h>
#include <Wire.h>

double IMU::accX, IMU::accY, IMU::accZ = 0;
double IMU::gyroX, IMU::gyroY, IMU::gyroZ = 0;
double IMU::roll, IMU::pitch, IMU::yaw = 0;
double IMU::gyroXangle, IMU::gyroYangle, IMU::gyroZangle = 0; // Angle calculate using the gyro only
double IMU::compAngleX, IMU::compAngleY, IMU::compAngleZ = 0; // Calculated angle using a complementary filter
double IMU::kalAngleX, IMU::kalAngleY, IMU::kalAngleZ = 0; // Calculated angle using a Kalman filter
double IMU::rollAngle, IMU::pitchAngle = 0;
double IMU::Bfy, IMU::Bfx = 0;
double IMU::gyroXrate, IMU::gyroYrate, IMU::gyroZrate = 0; 
int16_t IMU::tempRaw = 0;
uint8_t IMU::Data[14] = {0};

uint8_t MPU6050_address = 0x68; // If AD0 is logic low on the PCB the address is 0x68, otherwise set this to 0x69

/** Default constructor.
 */
IMU::IMU() {
}

void IMU::init(){
  while(!I2Cdev::writeByte(MPU6050_address, 0x19, 7));  //  Set the sample rate to 1000Hz - 8kHz/(7+1) = 1000Hz
  while(!I2Cdev::writeByte(MPU6050_address, 0x1A, 0x00)); //  Disable FSYNC and set 260 Hz Acc filtering, 256 Hz Gyro filtering, 8 KHz sampling
  while(!I2Cdev::writeByte(MPU6050_address, 0x1B, 0x00)); //  Set Gyro Full Scale Range to ±250deg/s
  while(!I2Cdev::writeByte(MPU6050_address, 0x1C, 0x00)); //  Set Accelerometer Full Scale Range to ±2g
  I2Cdev::writeBit(MPU6050_address, 0x37, 1, 1); // set bypass mode for gateway to hmc5883L
  I2Cdev::writeBit(MPU6050_address, 0x6A, 5, 0); // set bypass mode for gateway to hmc5883L
  while(!I2Cdev::writeByte(MPU6050_address, 0x6B, 0x01)); // PLL with X axis gyroscope reference and disable sleep mode
  
  while(!I2Cdev::readBytes(MPU6050_address, 0x75, 1, Data));
  if (Data[0] != 0x68) { // Read "WHO_AM_I" register
    Serial.print(F("MPU6050 connection failed"));
    while (1);
  }
  Serial.println("MPU6050 connection successful");
  delay(100); // Wait for sensors to stabilize
}


void IMU::getdata(){

  I2Cdev::readBytes(MPU6050_address, 0x3B, 14, IMU::Data); // Get accelerometer and gyroscope values
  IMU::accX = ((IMU::Data[0] << 8) | IMU::Data[1]);
  IMU::accY = -((IMU::Data[2] << 8) | IMU::Data[3]);
  IMU::accZ = ((IMU::Data[4] << 8) | IMU::Data[5]);
  IMU::tempRaw = (IMU::Data[6] << 8) | IMU::Data[7];
  IMU::gyroX = -(IMU::Data[8] << 8) | IMU::Data[9];
  IMU::gyroY = (IMU::Data[10] << 8) | IMU::Data[11];
  IMU::gyroZ = -(IMU::Data[12] << 8) | IMU::Data[13];

}

void IMU::updatePitchRoll(){

  IMU::roll = atan2(accY, accZ) * RAD_TO_DEG;
  IMU::pitch = atan2(-accX, accZ) * RAD_TO_DEG;

}

void IMU::updateYaw(){
  
  HMC5883L::magX *= -1; // Invert axis - this it done here, as it should be done after the calibration
  HMC5883L::magZ *= -1;

  HMC5883L::magX *= HMC5883L::magGain[0];
  HMC5883L::magY *= HMC5883L::magGain[1];
  HMC5883L::magZ *= HMC5883L::magGain[2];

  HMC5883L::magX -= HMC5883L::magOffset[0];
  HMC5883L::magY -= HMC5883L::magOffset[1];
  HMC5883L::magZ -= HMC5883L::magOffset[2];

  IMU::rollAngle = IMU::kalAngleX * DEG_TO_RAD;
  IMU::pitchAngle = IMU::kalAngleY * DEG_TO_RAD;

  IMU::Bfy = HMC5883L::magZ * sin(IMU::rollAngle) - HMC5883L::magY * cos(IMU::rollAngle);
  IMU::Bfx = HMC5883L::magX * cos(IMU::pitchAngle) + HMC5883L::magY * sin(IMU::pitchAngle) * sin(IMU::rollAngle) + HMC5883L::magZ * sin(IMU::pitchAngle) * cos(IMU::rollAngle);
  IMU::yaw = atan2(-IMU::Bfy, IMU::Bfx) * RAD_TO_DEG;

  IMU::yaw *= -1;

}
