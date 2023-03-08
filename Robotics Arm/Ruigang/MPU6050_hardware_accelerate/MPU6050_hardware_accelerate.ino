#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "TimerOne.h"

#define matrix_number 10
#define button_pin 18

/***** MPU variable *****/
MPU6050 mpu;  //MPU结构体初始化
uint8_t fifoBuffer[64];
Quaternion q;  //四元数结构体初始化
VectorFloat gravity;  
float ypr[3];
int16_t acc[3];
int16_t gyro[3];

float Previous_angle = 0;
float X_angle = 0;
float Y_angle = 0;
float Z_angle = 0;
int16_t X_velocity = 0;
int16_t Y_velocity = 0;
int16_t Z_velocity = 0;
/******************************/

/***** button variable *****/
char key_count = 0;
char key_state = 0;
/******************************/

/***** clutching variable *****/
int clutch_state = 0;
int clutch_timecount = 0;
char clutch_direction = 0;
/******************************/

/***** matrix for data variable *****/
float degree_matrix[matrix_number] = {};
int16_t speed_matrix[matrix_number] = {};
int stage_matrix[matrix_number] = {};
int time_matrix[matrix_number] = {};
int number_matrix = 0;
int start_state = 0;
/******************************/

/*
 * @brief: the function for the timer1 interrupt 
 * @return: nothing
 */
void Timer1_IRQHandler()
{
  if(clutch_state == 1){   //count the number and replace the delay()
    ++clutch_timecount;
  }  
  Savedata();
}

/*
 * @brief: the key function for key
 * @return: nothing
 */
void Key_function()  
{
  if(key_state == 1){
    delay(5);
    if(digitalRead(button_pin)){
      ++key_count;
      key_state = 0;
    }
  }

  switch(key_count){
  case 2:  //If you want to send the matrix data, just click the key twice.
    noInterrupts();
    Serial.print("Start Sending\n");
    Serial.print("angle = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(degree_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");

    // Serial.print("velocity = np.array([");
    // for (int i = 0; i < number_matrix; i++) {
    //   Serial.print(speed_matrix[i]);
    //   Serial.print(", ");
    // }
    // Serial.print("])\n");
    // Serial.print("stage = np.array([");
    // for (int i = 0; i < number_matrix; i++) {
    //   Serial.print(stage_matrix[i]);
    //   Serial.print(", ");
    // }
    // Serial.print("])\n");

    Serial.print("time = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(time_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");
    Serial.print("Finish Sending\n");
    key_count++;
    interrupts();
    break;  
  case 3:
    key_count = 0;
    break;      
  default:
    break;
  }

}

/*
 * @brief: the IRQ Handler for key
 * @return: nothing
 */
void Key_IRQHandler()  
{
  key_state = 1;
}

/*
 * @brief: Sending the MPU data in serial
 * @return: nothing
 */
void MPU_datasend()
{
  Serial.print("90 degree:");Serial.println(90);
  Serial.print("-90 degree:");Serial.println(-90);

  // Serial.print("Pitch:");Serial.println(X_angle); //x direction
  // Serial.print("Roll:");Serial.println(Y_angle);  //y direction
  // Serial.print("Yaw:");Serial.println(Z_angle);  //z direction

  // Serial.print("accx:");Serial.println(acc[0]); //x direction
  // Serial.print("accy:");Serial.println(acc[1]); //y direction
  
  // Serial.print("gyrox:");Serial.println(X_velocity); //x direction
  // Serial.print("gyroy:");Serial.println(Y_velocity); //y direction
  // Serial.print("gyroz:");Serial.println(Z_velocity); //z direction
    
    Serial.print("Yaw:");Serial.println(Z_angle);  //z direction
}

/*
 * @brief: Get the data from the register of MPU
 * @return: nothing
 */
void MPU_getdata()
{
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer))
  {
    mpu.dmpGetQuaternion(&q, fifoBuffer);  //获取四元数
    mpu.dmpGetGravity(&gravity, &q);  
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

    mpu.dmpGetAccel(acc,fifoBuffer);  //获取加速度
    mpu.dmpGetGyro(gyro,fifoBuffer);  //获取角速度

    X_angle = ypr[1] * 180 / M_PI;
    Y_angle = ypr[2] * 180 / M_PI;
    Z_angle = ypr[0] * 180 / M_PI;

    X_velocity = gyro[1];
    Y_velocity = gyro[0];
    Z_velocity = gyro[2];

  }
}

/*
 * @brief: Set the speed interval to let the magnet clutch the stick in advance.
 * @return: nothing
 */
void SpeedCluthingmethod()
{
  if(-Z_velocity < 40 && -Z_velocity > 0 && clutch_direction == 1 && start_state == 1 && Z_angle > 0){
    clutch_state = 1;
    clutch_direction = 0;
  }

  if(-Z_velocity > -40 && -Z_velocity < 0 && clutch_direction == 0 && start_state == 1 && Z_angle < 0){
    clutch_state = 1;
    clutch_direction = 1;
  }
}
/*
 * @brief: Save data to matrix
 * @return: nothing
 */
void Savedata()
{
  if(Previous_angle < (Z_angle-0.5) && start_state == 0){
    start_state = 1;
    clutch_direction = 1;
  }
  if(number_matrix < matrix_number && start_state == 1){
    static int start_time = millis();
    degree_matrix[number_matrix] = Z_angle;
    // speed_matrix[number_matrix] = -Z_velocity;
    // stage_matrix[number_matrix] = clutch_state;
    time_matrix[number_matrix] = millis() - start_time;
    number_matrix++;
  }
  Previous_angle = Z_angle;
}

void setup()
{
  
  Serial.begin(115200);
  
  Serial.print("\n**** Start To Init The System... ****\n\n");

  mpu.initialize();
  Serial.print("The device:");
  Serial.print(mpu.testConnection());
  Serial.print("\n");
  mpu.dmpInitialize();
  
  Serial.print("**** The System Init Done... ****\n");
  mpu.CalibrateAccel(6);
  mpu.CalibrateGyro(6);
  
  mpu.PrintActiveOffsets();
  mpu.setDMPEnabled(true);
  
  pinMode(button_pin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button_pin),Key_IRQHandler, FALLING);

  Timer1.initialize(10000); // 初始化 Timer1 ，定时器每间隔 10ms（10000us = 10ms）执行中断函数一次
  Timer1.attachInterrupt(Timer1_IRQHandler);

  Serial.print("**** The System Init Done... ****\n");
}


void loop()
{ 
  Key_function();
  MPU_getdata();
  MPU_datasend();
  // SpeedCluthingmethod();
  
  if(clutch_state == 1){
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 100){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0);
    }
  }
}