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
  // Serial.print("kalAngleZ:");Serial.println((int)IMU::kalAngleZ);
  // Serial.print("compAngleZ:");Serial.println((int)IMU::compAngleZ);
  // Serial.print("Yaw:");Serial.println(IMU::yaw);
  delay(10);
}

