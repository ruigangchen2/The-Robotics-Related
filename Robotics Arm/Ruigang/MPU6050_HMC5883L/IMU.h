#ifndef _IMU_H_
#define _IMU_H_
#include <stdint.h>


class IMU {
    public:
        IMU();
        
        static void init();
        static void getdata();
        static void updatePitchRoll();
        static void updateYaw();
        static void Kalmaninitialize();
        static void InvertEulerangle();
        static void Quaternion();
        static void MahonyAHRSupdate(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz, double dt);
        static void MahonyAHRSupdateIMU(float gx, float gy, float gz, float ax, float ay, float az, double dt);
        static float invSqrt(float x);
        static void kalman_1(struct _1_ekf_filter *ekf,float input);

        static double accX, accY, accZ;
        static double gyroX, gyroY, gyroZ;
        static double roll, pitch, yaw;
        
        static double gyroXangle, gyroYangle, gyroZangle; // Angle calculate using the gyro only
        static double compAngleX, compAngleY, compAngleZ; // Calculated angle using a complementary filter
        static double kalAngleX, kalAngleY, kalAngleZ; // Calculated angle using a Kalman filter
        static double rollAngle, pitchAngle;
        static double Bfy, Bfx;
        static double gyroXrate, gyroYrate, gyroZrate; 

        static int16_t tempRaw;
        static uint8_t Data[14];
    private:


};

#endif