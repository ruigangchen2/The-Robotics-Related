#include <Wire.h>
#include "Kalman.h" 
#include "I2Cdev.h"
#include "HMC5883L.h"
#include "IMU.h"

Kalman kalmanX, kalmanY, kalmanZ; // Create the Kalman instances
uint32_t timer;



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

  kalmanX.setAngle(IMU::roll); // First set roll starting angle
  IMU::gyroXangle = IMU::roll;
  IMU::compAngleX = IMU::roll;

  kalmanY.setAngle(IMU::pitch); // Then pitch
  IMU::gyroYangle = IMU::pitch;
  IMU::compAngleY = IMU::pitch;

  kalmanZ.setAngle(IMU::yaw); // And finally yaw
  IMU::gyroZangle = IMU::yaw;
  IMU::compAngleZ = IMU::yaw;

  timer = micros(); // Initialize the timer
}

void loop() {
  /* Update all the IMU values */
  IMU::getdata();
  HMC5883L::getdata();
  double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
  timer = micros();

  /* Roll and pitch estimation */
  IMU::updatePitchRoll();
  
  IMU::gyroXrate = IMU::gyroX / 131.0; // Convert to deg/s
  IMU::gyroYrate = IMU::gyroY / 131.0; // Convert to deg/s

  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((IMU::roll < -90 && IMU::kalAngleX > 90) || (IMU::roll > 90 && IMU::kalAngleX < -90)) {
    kalmanX.setAngle(IMU::roll);
    IMU::compAngleX = IMU::roll;
    IMU::kalAngleX = IMU::roll;
    IMU::gyroXangle = IMU::roll;
  } else
    IMU::kalAngleX = kalmanX.getAngle(IMU::roll, IMU::gyroXrate, dt); // Calculate the angle using a Kalman filter

  if (abs(IMU::kalAngleX) > 90)
    IMU::gyroYrate = -IMU::gyroYrate; // Invert rate, so it fits the restricted accelerometer reading
  IMU::kalAngleY = kalmanY.getAngle(IMU::pitch, IMU::gyroYrate, dt);
  // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
  if ((IMU::pitch < -90 && IMU::kalAngleY > 90) || (IMU::pitch > 90 && IMU::kalAngleY < -90)) {
    kalmanY.setAngle(IMU::pitch);
    IMU::compAngleY = IMU::pitch;
    IMU::kalAngleY = IMU::pitch;
    IMU::gyroYangle = IMU::pitch;
  } else
    IMU::kalAngleY = kalmanY.getAngle(IMU::pitch,IMU::gyroYrate, dt); // Calculate the angle using a Kalman filter

  if (abs(IMU::kalAngleY) > 90)
    IMU::gyroXrate = -IMU::gyroXrate; // Invert rate, so it fits the restricted accelerometer reading
  IMU::kalAngleX = kalmanX.getAngle(IMU::roll, IMU::gyroXrate, dt); // Calculate the angle using a Kalman filter



  /* Yaw estimation */
  IMU::updateYaw();
  IMU::gyroZrate = IMU::gyroZ / 131.0; // Convert to deg/s
  // This fixes the transition problem when the yaw angle jumps between -180 and 180 degrees
  if ((IMU::yaw < -90 && IMU::kalAngleZ > 90) || (IMU::yaw > 90 && IMU::kalAngleZ < -90)) {
    kalmanZ.setAngle(IMU::yaw);
    IMU::compAngleZ = IMU::yaw;
    IMU::kalAngleZ = IMU::yaw;
    IMU::gyroZangle = IMU::yaw;
  } else
    IMU::kalAngleZ = kalmanZ.getAngle(IMU::yaw, IMU::gyroZrate, dt); // Calculate the angle using a Kalman filter


  /* Estimate angles using gyro only */
  IMU::gyroXangle += IMU::gyroXrate * dt; // Calculate gyro angle without any filter
  IMU::gyroYangle += IMU::gyroYrate * dt;
  IMU::gyroZangle += IMU::gyroZrate * dt;
  //gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate from the Kalman filter
  //gyroYangle += kalmanY.getRate() * dt;
  //gyroZangle += kalmanZ.getRate() * dt;

  /* Estimate angles using complimentary filter */
  IMU::compAngleX = 0.93 * (IMU::compAngleX + IMU::gyroXrate * dt) + 0.07 * IMU::roll; // Calculate the angle using a Complimentary filter
  IMU::compAngleY = 0.93 * (IMU::compAngleY + IMU::gyroYrate * dt) + 0.07 * IMU::pitch;
  IMU::compAngleZ = 0.93 * (IMU::compAngleZ + IMU::gyroZrate * dt) + 0.07 * IMU::yaw;

  // Reset the gyro angles when they has drifted too much
  if (IMU::gyroXangle < -180 || IMU::gyroXangle > 180)
    IMU::gyroXangle = IMU::kalAngleX;
  if (IMU::gyroYangle < -180 || IMU::gyroYangle > 180)
    IMU::gyroYangle = IMU::kalAngleY;
  if (IMU::gyroZangle < -180 || IMU::gyroZangle > 180)
   IMU::gyroZangle = IMU::kalAngleZ;


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




