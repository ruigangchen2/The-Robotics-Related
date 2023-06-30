//
// MPU-9250 Mahony AHRS  S.J. Remington 3/2020
// last update 12/17/2020
// added full matrix calibration for accel and mag
// See: http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/
// ***Standard orientation defined by gyro/accel: X North Y West Z Up***

// VERY VERY IMPORTANT!
// Both the accelerometer and magnetometer MUST be properly calibrated for this program to work, and the gyro offset must be determned.
// Follow the procedure described in http://sailboatinstruments.blogspot.com/2011/08/improved-magnetometer-calibration.html
// or in more detail, the tutorial https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
//
// To collect data for calibration, use the companion programs MPU9250_cal and Magneto 1.2 from sailboatinstruments.blogspot.com
//
// For correcting the data, below I use the diagonal element of matrix A and ignore
// the off diagonal components. If those terms are large, (most likely only for the magnetometer)
// add them in to the corrections in function get_MPU_scaled()
//
// This version must be compiled with library routines in subfolder "libs"

#include "Wire.h"
// I2Cdev and MPU9250 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "libs/I2Cdev.cpp"
#include "libs/MPU9250.cpp"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for Sparkfun module)
// AD0 high = 0x69
// MAHONY FILTER SELECTED BELOW

MPU9250 accelgyro;
I2Cdev   I2C_M;

// vvvvvvvvvvvvvvvvvv  VERY VERY IMPORTANT vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
//These are the previously determined offsets and scale factors for accelerometer and magnetometer, using MPU9250_cal and Magneto 1.2
//The AHRS will NOT work well or at all if these are not correct
//
// redetermined 12/16/2020
//acel offsets and correction matrix
 float A_B[3] {  539.75,  218.36,  834.53}; 
 float A_Ainv[3][3]
  {{  0.51280,  0.00230,  0.00202},
  {  0.00230,  0.51348, -0.00126},
  {  0.00202, -0.00126,  0.50368}};
  
// mag offsets and correction matrix
  float M_B[3]
 {   18.15,   28.05,  -36.09};
 float M_Ainv[3][3]
 {{  0.68093,  0.00084,  0.00923},
  {  0.00084,  0.69281,  0.00103},
  {  0.00923,  0.00103,  0.64073}};
  
  float G_off[3] = {-299.7, 113.2, 202.4}; //raw offsets, determined for gyro at rest
// ^^^^^^^^^^^^^^^^^^^ VERY VERY IMPORTANT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

char s[60]; //snprintf buffer
//raw data and scaled as vector
int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;
float Axyz[3];
float Gxyz[3];
float Mxyz[3];
#define gscale (250./32768.0)*(PI/180.0)  //gyro default 250 LSB per d/s -> rad/s

// NOW USING MAHONY FILTER

// These are the free parameters in the Mahony filter and fusion scheme,
// Kp for proportional feedback, Ki for integral
// with MPU-9250, angles start oscillating at Kp=40. Ki does not seem to help and is not required.
#define Kp 30.0
#define Ki 0.0

// globals for AHRS loop timing

unsigned long now = 0, last = 0; //micros() timers
float deltat = 0;  //loop time in seconds
unsigned long now_ms, last_ms = 0; //millis() timers
unsigned long print_ms = 10; //print every "print_ms" milliseconds


// Vector to hold quaternion
static float q[4] = {1.0, 0.0, 0.0, 0.0};
static float yaw, pitch, roll; //Euler angle output

void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
  Wire.begin();
  Serial.begin(9600);
  while(!Serial); //wait for connection

  // initialize device
  accelgyro.initialize();
  // verify connection
  Serial.println(accelgyro.testConnection() ? "MPU9250 OK" : "MPU9250 ??");
}

// AHRS loop

void loop()
{
  get_MPU_scaled();
  now = micros();
  deltat = (now - last) * 1.0e-6; //seconds since last update
  last = now;

  // correct for differing accelerometer and magnetometer alignment by circularly permuting mag axes

  MahonyQuaternionUpdate(Axyz[0], Axyz[1], Axyz[2], Gxyz[0], Gxyz[1], Gxyz[2],
                         Mxyz[1], Mxyz[0], -Mxyz[2], deltat);
  //  Standard orientation: X North, Y West, Z Up
  //  Tait-Bryan angles as well as Euler angles are
  // non-commutative; that is, the get the correct orientation the rotations
  // must be applied in the correct order which for this configuration is yaw,
  // pitch, and then roll.
  // http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
  // which has additional links.
 
  // Strictly valid only for approximately level movement       
  // WARNING: This angular conversion is for DEMONSTRATION PURPOSES ONLY. It WILL
  // MALFUNCTION for certain combinations of angles! See https://en.wikipedia.org/wiki/Gimbal_lock
  roll  = atan2((q[0] * q[1] + q[2] * q[3]), 0.5 - (q[1] * q[1] + q[2] * q[2]));
  pitch = asin(2.0 * (q[0] * q[2] - q[1] * q[3]));
  yaw   = atan2((q[1] * q[2] + q[0] * q[3]), 0.5 - ( q[2] * q[2] + q[3] * q[3]));
  // to degrees
  yaw   *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll *= 180.0 / PI;

  // http://www.ngdc.noaa.gov/geomag-web/#declination
  //conventional nav, yaw increases CW from North, corrected for local magnetic declination

  yaw = -yaw + 14.5;
  if(yaw<0) yaw += 360.0;
  if(yaw>360.0) yaw -= 360.0;
  now_ms = millis(); //time to print?
  if (now_ms - last_ms >= print_ms) {
    last_ms = now_ms;
    // print angles for serial plotter...
    //  Serial.print("ypr ");
    Serial.print(yaw, 0);
    Serial.print(", ");
    Serial.print(pitch, 0);
    Serial.print(", ");
    Serial.println(roll, 0);
  }
}

void get_MPU_scaled(void) {
  float temp[3];
  int i;
  accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

  Gxyz[0] = ((float) gx - G_off[0]) * gscale; //250 LSB(d/s) default to radians/s
  Gxyz[1] = ((float) gy - G_off[1]) * gscale;
  Gxyz[2] = ((float) gz - G_off[2]) * gscale;

  Axyz[0] = (float) ax;
  Axyz[1] = (float) ay;
  Axyz[2] = (float) az;
  //apply offsets (bias) and scale factors from Magneto
  for (i = 0; i < 3; i++) temp[i] = (Axyz[i] - A_B[i]);
  Axyz[0] = A_Ainv[0][0] * temp[0] + A_Ainv[0][1] * temp[1] + A_Ainv[0][2] * temp[2];
  Axyz[1] = A_Ainv[1][0] * temp[0] + A_Ainv[1][1] * temp[1] + A_Ainv[1][2] * temp[2];
  Axyz[2] = A_Ainv[2][0] * temp[0] + A_Ainv[2][1] * temp[1] + A_Ainv[2][2] * temp[2];
  vector_normalize(Axyz);

  Mxyz[0] = (float) mx;
  Mxyz[1] = (float) my;
  Mxyz[2] = (float) mz;
  //apply offsets and scale factors from Magneto
  for (i = 0; i < 3; i++) temp[i] = (Mxyz[i] - M_B[i]);
  Mxyz[0] = M_Ainv[0][0] * temp[0] + M_Ainv[0][1] * temp[1] + M_Ainv[0][2] * temp[2];
  Mxyz[1] = M_Ainv[1][0] * temp[0] + M_Ainv[1][1] * temp[1] + M_Ainv[1][2] * temp[2];
  Mxyz[2] = M_Ainv[2][0] * temp[0] + M_Ainv[2][1] * temp[1] + M_Ainv[2][2] * temp[2];
  vector_normalize(Mxyz);
 }

// Mahony scheme uses proportional and integral filtering on
// the error between estimated reference vectors and measured ones.
void MahonyQuaternionUpdate(float ax, float ay, float az, float gx, float gy, float gz, float mx, float my, float mz, float deltat)
{
  // Vector to hold integral error for Mahony method
  static float eInt[3] = {0.0, 0.0, 0.0};
  // short name local variable for readability
  float q1 = q[0], q2 = q[1], q3 = q[2], q4 = q[3];
  float norm;
  float hx, hy, bx, bz;
  float vx, vy, vz, wx, wy, wz;
  float ex, ey, ez;
  float pa, pb, pc;

  // Auxiliary variables to avoid repeated arithmetic
  float q1q1 = q1 * q1;
  float q1q2 = q1 * q2;
  float q1q3 = q1 * q3;
  float q1q4 = q1 * q4;
  float q2q2 = q2 * q2;
  float q2q3 = q2 * q3;
  float q2q4 = q2 * q4;
  float q3q3 = q3 * q3;
  float q3q4 = q3 * q4;
  float q4q4 = q4 * q4;
  /*
    // already done in loop()

    // Normalise accelerometer measurement
    norm = sqrt(ax * ax + ay * ay + az * az);
    if (norm == 0.0f) return; // Handle NaN
    norm = 1.0f / norm;       // Use reciprocal for division
    ax *= norm;
    ay *= norm;
    az *= norm;

    // Normalise magnetometer measurement
    norm = sqrt(mx * mx + my * my + mz * mz);
    if (norm == 0.0f) return; // Handle NaN
    norm = 1.0f / norm;       // Use reciprocal for division
    mx *= norm;
    my *= norm;
    mz *= norm;
  */
  // Reference direction of Earth's magnetic field
  hx = 2.0f * mx * (0.5f - q3q3 - q4q4) + 2.0f * my * (q2q3 - q1q4) + 2.0f * mz * (q2q4 + q1q3);
  hy = 2.0f * mx * (q2q3 + q1q4) + 2.0f * my * (0.5f - q2q2 - q4q4) + 2.0f * mz * (q3q4 - q1q2);
  bx = sqrt((hx * hx) + (hy * hy));
  bz = 2.0f * mx * (q2q4 - q1q3) + 2.0f * my * (q3q4 + q1q2) + 2.0f * mz * (0.5f - q2q2 - q3q3);

  // Estimated direction of gravity and magnetic field
  vx = 2.0f * (q2q4 - q1q3);
  vy = 2.0f * (q1q2 + q3q4);
  vz = q1q1 - q2q2 - q3q3 + q4q4;
  wx = 2.0f * bx * (0.5f - q3q3 - q4q4) + 2.0f * bz * (q2q4 - q1q3);
  wy = 2.0f * bx * (q2q3 - q1q4) + 2.0f * bz * (q1q2 + q3q4);
  wz = 2.0f * bx * (q1q3 + q2q4) + 2.0f * bz * (0.5f - q2q2 - q3q3);

  // Error is cross product between estimated direction and measured direction of the reference vectors
  ex = (ay * vz - az * vy) + (my * wz - mz * wy);
  ey = (az * vx - ax * vz) + (mz * wx - mx * wz);
  ez = (ax * vy - ay * vx) + (mx * wy - my * wx);
  if (Ki > 0.0f)
  {
    eInt[0] += ex;      // accumulate integral error
    eInt[1] += ey;
    eInt[2] += ez;
    // Apply I feedback
    gx += Ki*eInt[0];
    gy += Ki*eInt[1];
    gz += Ki*eInt[2];
  }


  // Apply P feedback
  gx = gx + Kp * ex; 
  gy = gy + Kp * ey;
  gz = gz + Kp * ez;

// Integrate rate of change of quaternion
 // small correction 1/11/2022, see https://github.com/kriswiner/MPU9250/issues/447
gx = gx * (0.5*deltat); // pre-multiply common factors
gy = gy * (0.5*deltat);
gz = gz * (0.5*deltat);
float qa = q1;
float qb = q2;
float qc = q3;
q1 += (-qb * gx - qc * gy - q4 * gz);
q2 += (qa * gx + qc * gz - q4 * gy);
q3 += (qa * gy - qb * gz + q4 * gx);
q4 += (qa * gz + qb * gy - qc * gx);

  // Normalise quaternion
  norm = sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4);
  norm = 1.0f / norm;
  q[0] = q1 * norm;
  q[1] = q2 * norm;
  q[2] = q3 * norm;
  q[3] = q4 * norm;
}

float vector_dot(float a[3], float b[3])
{
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

void vector_normalize(float a[3])
{
  float mag = sqrt(vector_dot(a, a));
  a[0] /= mag;
  a[1] /= mag;
  a[2] /= mag;
}
