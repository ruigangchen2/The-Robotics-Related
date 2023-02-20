#include <Wire.h>
#include "Kalman.h" 
#include "I2Cdev.h"
#include "HMC5883L.h"
#include "IMU.h"

void setup() {
  delay(100); // Wait for sensors to get ready

  Serial.begin(115200);
  Wire.begin();

  IMU::init();  //Init the MPU6050

  HMC5883L::setmode_continuous();// Configure device for continuous mode
  HMC5883L::calibrate(); //calibrate the HMC
  
  /* Set Kalman and gyro starting angle */
  IMU::getdata();
  HMC5883L::getdata();
  
  IMU::updatePitchRoll();
  IMU::updateYaw();
  IMU::Kalmaninitialize();
}

void loop() {

  IMU::InvertEulerangle();

  /* Print Data */
#if 1
  Serial.print(IMU::roll); Serial.print("\t");
  Serial.print(IMU::gyroXangle); Serial.print("\t");
  Serial.print(IMU::compAngleX); Serial.print("\t");
  Serial.print(IMU::kalAngleX); Serial.print("\t");

  Serial.print("\t");

  Serial.print(IMU::pitch); Serial.print("\t");
  Serial.print(IMU::gyroYangle); Serial.print("\t");
  Serial.print(IMU::compAngleY); Serial.print("\t");
  Serial.print(IMU::kalAngleY); Serial.print("\t");

  Serial.print("\t");

  Serial.print(IMU::yaw); Serial.print("\t");
  Serial.print(IMU::gyroZangle); Serial.print("\t");
  Serial.print(IMU::compAngleZ); Serial.print("\t");
  Serial.print(IMU::kalAngleZ); Serial.print("\t");
  Serial.print("\n");
#endif
  delay(10);
}

