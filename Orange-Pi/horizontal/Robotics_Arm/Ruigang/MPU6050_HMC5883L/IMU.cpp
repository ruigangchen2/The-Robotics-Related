#include "IMU.h"
#include "I2Cdev.h"
#include "HMC5883L.h"
#include "Kalman.h"
#include <Arduino.h>
#include <Wire.h>

Kalman kalmanX, kalmanY, kalmanZ; // Create the Kalman instances
uint32_t timer;

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


//---------------------------------------------------------------------------------------------------
// quaternion definition
#define twoKpDef	(2.0f * 0.5f)	// 2 * proportional gain
#define twoKiDef	(2.0f * 0.0f)	// 2 * integral gain

volatile float twoKp = twoKpDef;											// 2 * proportional gain (Kp)
volatile float twoKi = twoKiDef;											// 2 * integral gain (Ki)
volatile float q0 = 1.0f, q1 = 0.0f, q2 = 0.0f, q3 = 0.0f;					// quaternion of sensor frame relative to auxiliary frame
volatile float integralFBx = 0.0f,  integralFBy = 0.0f, integralFBz = 0.0f;	// integral error terms scaled by Ki


struct _1_ekf_filter
  {
    float LastP;	
    float	Now_P;	//测量不确定性
    float out;
    float Kg;		//卡尔曼增益
    float Q;	//过程噪声的方差
    float R;	//估计不确定性
  };
static struct _1_ekf_filter Kalman_parameter[9] = {{0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03},  //加速度计卡尔曼参数
																									 {0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03},	//陀螺仪卡尔曼参数
                                                   {0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03},{0.003,0,0,0,0.001,0.03}}; //磁力计

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

void IMU::Kalmaninitialize(){
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

void IMU::InvertEulerangle(){
  /* Update all the IMU values */
  IMU::getdata();
  HMC5883L::getdata();
  double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
  timer = micros();

  IMU::updatePitchRoll();
  IMU::gyroXrate = IMU::gyroX / 131.0; // Convert to deg/s
  IMU::gyroYrate = IMU::gyroY / 131.0; // Based on the setting. (131LSB)

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
  IMU::gyroZrate = IMU::gyroZ / 131.0; // Convert to deg/s. 131LSB

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
  // IMU::gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate from the Kalman filter
  // IMU::gyroYangle += kalmanY.getRate() * dt;
  // IMU::gyroZangle += kalmanZ.getRate() * dt;

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
}

void IMU::Quaternion(){
  uint8_t buffer[9];
  IMU::getdata();
  HMC5883L::getdata();
  buffer[0] = IMU::accX;
  buffer[1] = IMU::accY;
  buffer[2] = IMU::accZ;
  buffer[3] = IMU::gyroX;
  buffer[4] = IMU::gyroY;
  buffer[5] = IMU::gyroZ;
  buffer[6] = HMC5883L::magX;
  buffer[7] = HMC5883L::magY;
  buffer[8] = HMC5883L::magZ;
  for(int i=0;i<9;i++){
    kalman_1(&Kalman_parameter[i],(float)buffer[i]);  //一维卡尔曼滤波
    buffer[i] = (int16_t)Kalman_parameter[i].out;  //滤波结果输出
  }
  double dt = (double)(micros() - timer) / 1000000; // unit : seconds
  timer = micros();
  IMU::MahonyAHRSupdate(buffer[3] * DEG_TO_RAD, buffer[4] * DEG_TO_RAD, buffer[5] * DEG_TO_RAD, buffer[0], buffer[1], buffer[2], buffer[6], buffer[7], buffer[8], dt);

#if 1
  Serial.print("PITCH:");Serial.println(IMU::pitch);
  // Serial.print(IMU::roll); Serial.print("\n");
  // Serial.print(IMU::yaw); Serial.print("\n");

#endif
}

void IMU::MahonyAHRSupdateIMU(float gx, float gy, float gz, float ax, float ay, float az, double dt){
	float recipNorm;
	float halfvx, halfvy, halfvz;
	float halfex, halfey, halfez;
	float qa, qb, qc;

	// Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
	if(!((ax == 0.0f) && (ay == 0.0f) && (az == 0.0f))) {

		// Normalise accelerometer measurement
		recipNorm = invSqrt(ax * ax + ay * ay + az * az);
		ax *= recipNorm;
		ay *= recipNorm;
		az *= recipNorm;        

		// Estimated direction of gravity and vector perpendicular to magnetic flux
		halfvx = q1 * q3 - q0 * q2;
		halfvy = q0 * q1 + q2 * q3;
		halfvz = q0 * q0 - 0.5f + q3 * q3;
	
		// Error is sum of cross product between estimated and measured direction of gravity
		halfex = (ay * halfvz - az * halfvy);
		halfey = (az * halfvx - ax * halfvz);
		halfez = (ax * halfvy - ay * halfvx);

		// Compute and apply integral feedback if enabled
		if(twoKi > 0.0f) {
			integralFBx += twoKi * halfex * dt;	// integral error scaled by Ki
			integralFBy += twoKi * halfey * dt;
			integralFBz += twoKi * halfez * dt;
			gx += integralFBx;	// apply integral feedback
			gy += integralFBy;
			gz += integralFBz;
		}
		else {
			integralFBx = 0.0f;	// prevent integral windup
			integralFBy = 0.0f;
			integralFBz = 0.0f;
		}

		// Apply proportional feedback
		gx += twoKp * halfex;
		gy += twoKp * halfey;
		gz += twoKp * halfez;
	}
	
	// Integrate rate of change of quaternion
	gx *= (0.5f * dt);		// pre-multiply common factors
	gy *= (0.5f * dt);
	gz *= (0.5f * dt);
	qa = q0;
	qb = q1;
	qc = q2;
	q0 += (-qb * gx - qc * gy - q3 * gz);
	q1 += (qa * gx + qc * gz - q3 * gy);
	q2 += (qa * gy - qb * gz + q3 * gx);
	q3 += (qa * gz + qb * gy - qc * gx); 
	
	// Normalise quaternion
	recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
	q0 *= recipNorm;
	q1 *= recipNorm;
	q2 *= recipNorm;
	q3 *= recipNorm;
}


void IMU::MahonyAHRSupdate(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz, double dt){
  float recipNorm;
  float q0q0, q0q1, q0q2, q0q3, q1q1, q1q2, q1q3, q2q2, q2q3, q3q3;  
	float hx, hy, bx, bz;
	float halfvx, halfvy, halfvz, halfwx, halfwy, halfwz;
	float halfex, halfey, halfez;
	float qa, qb, qc;


	// Use IMU algorithm if magnetometer measurement invalid (avoids NaN in magnetometer normalisation)
	if((mx == 0.0f) && (my == 0.0f) && (mz == 0.0f)) {
		MahonyAHRSupdateIMU(gx, gy, gz, ax, ay, az, dt);
		return;
	}

	// Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
	if(!((ax == 0.0f) && (ay == 0.0f) && (az == 0.0f))) {

		// Normalise accelerometer measurement
		recipNorm = invSqrt(ax * ax + ay * ay + az * az);
		ax *= recipNorm;
		ay *= recipNorm;
		az *= recipNorm;     

		// Normalise magnetometer measurement
		recipNorm = invSqrt(mx * mx + my * my + mz * mz);
		mx *= recipNorm;
		my *= recipNorm;
		mz *= recipNorm;   

        // Auxiliary variables to avoid repeated arithmetic
        q0q0 = q0 * q0;
        q0q1 = q0 * q1;
        q0q2 = q0 * q2;
        q0q3 = q0 * q3;
        q1q1 = q1 * q1;
        q1q2 = q1 * q2;
        q1q3 = q1 * q3;
        q2q2 = q2 * q2;
        q2q3 = q2 * q3;
        q3q3 = q3 * q3;   

        // Reference direction of Earth's magnetic field
        hx = 2.0f * (mx * (0.5f - q2q2 - q3q3) + my * (q1q2 - q0q3) + mz * (q1q3 + q0q2));
        hy = 2.0f * (mx * (q1q2 + q0q3) + my * (0.5f - q1q1 - q3q3) + mz * (q2q3 - q0q1));
        bx = sqrt(hx * hx + hy * hy);
        bz = 2.0f * (mx * (q1q3 - q0q2) + my * (q2q3 + q0q1) + mz * (0.5f - q1q1 - q2q2));

		// Estimated direction of gravity and magnetic field
		halfvx = q1q3 - q0q2;
		halfvy = q0q1 + q2q3;
		halfvz = q0q0 - 0.5f + q3q3;
        halfwx = bx * (0.5f - q2q2 - q3q3) + bz * (q1q3 - q0q2);
        halfwy = bx * (q1q2 - q0q3) + bz * (q0q1 + q2q3);
        halfwz = bx * (q0q2 + q1q3) + bz * (0.5f - q1q1 - q2q2);  
	
		// Error is sum of cross product between estimated direction and measured direction of field vectors
		halfex = (ay * halfvz - az * halfvy) + (my * halfwz - mz * halfwy);
		halfey = (az * halfvx - ax * halfvz) + (mz * halfwx - mx * halfwz);
		halfez = (ax * halfvy - ay * halfvx) + (mx * halfwy - my * halfwx);

		// Compute and apply integral feedback if enabled
		if(twoKi > 0.0f) {
			integralFBx += twoKi * halfex * dt;	// integral error scaled by Ki
			integralFBy += twoKi * halfey * dt;
			integralFBz += twoKi * halfez * dt;
			gx += integralFBx;	// apply integral feedback
			gy += integralFBy;
			gz += integralFBz;
		}
		else {
			integralFBx = 0.0f;	// prevent integral windup
			integralFBy = 0.0f;
			integralFBz = 0.0f;
		}

		// Apply proportional feedback
		gx += twoKp * halfex;
		gy += twoKp * halfey;
		gz += twoKp * halfez;
	}
	
	// Integrate rate of change of quaternion
	gx *= (0.5f * dt);		// pre-multiply common factors
	gy *= (0.5f * dt);
	gz *= (0.5f * dt);
	qa = q0;
	qb = q1;
	qc = q2;
	q0 += (-qb * gx - qc * gy - q3 * gz);
	q1 += (qa * gx + qc * gz - q3 * gy);
	q2 += (qa * gy - qb * gz + q3 * gx);
	q3 += (qa * gz + qb * gy - qc * gx); 
	
	// Normalise quaternion
	recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
	q0 *= recipNorm;
	q1 *= recipNorm;
	q2 *= recipNorm;
	q3 *= recipNorm;

  {  
    IMU::yaw = -atan2f(2*q1*q2 + 2*q0*q3, -2*q2*q2 - 2*q3*q3 + 1) * RAD_TO_DEG;
    IMU::roll = atan2f(2*q2*q3 + 2*q0*q1, -2*q1*q1 - 2*q2*q2 + 1) * RAD_TO_DEG;
    IMU::pitch = -asin(-2*q1*q3 + 2*q0*q2) * RAD_TO_DEG;
  }
}


float IMU::invSqrt(float x) {
	float halfx = 0.5f * x;
	float y = x;
	long i = *(long*)&y;
	i = 0x5f3759df - (i>>1);
	y = *(float*)&i;
	y = y * (1.5f - (halfx * y * y));
	return y;
}

void IMU::kalman_1(struct _1_ekf_filter *ekf, float input){ //一维卡尔曼
	ekf->Now_P = ekf->LastP + ekf->Q;   								//p(x,x-1) = p(x-1,x-1) + Q   更新外推不确定性
	
	ekf->Kg = ekf->Now_P / (ekf->Now_P + ekf->R);				//K = p / (p + R)   更新卡尔曼增益，
	
	ekf->out = ekf->out + ekf->Kg * (input - ekf->out); //卡尔曼状态更新方程
	
	ekf->LastP = (1-ekf->Kg) * ekf->Now_P ;							//估计不确定性更新
}

