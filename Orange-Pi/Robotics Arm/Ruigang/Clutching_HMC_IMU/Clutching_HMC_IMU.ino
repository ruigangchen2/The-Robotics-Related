#include <Wire.h>
#include "Kalman.h" 
#include "I2Cdev.h"
#include "HMC5883L.h"
#include "IMU.h"
#include "TimerOne.h"

#define matrix_number 1100
#define button_pin 18


float Previous_angle = 0;
float yaw_angle = 0;
float yaw_speed = 0;
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
    // Serial.print("angle = np.array([");
    // for (int i = 0; i < number_matrix; i++) {
    //   Serial.print(degree_matrix[i]);
    //   Serial.print(", ");
    // }
    // Serial.print("])\n");

    Serial.print("velocity = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(speed_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");

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
 * @brief: Set the speed interval to let the magnet clutch the stick in advance.
 * @return: nothing
 */
void SpeedCluthingmethod()
{
  if(yaw_speed < 10 && yaw_speed > 0 && clutch_direction == 1 && start_state == 1 && yaw_angle > 0){
    clutch_state = 1;
    clutch_direction = 0;
  }

  if(yaw_speed > -10 && yaw_speed < 0 && clutch_direction == 0 && start_state == 1 && yaw_angle < 0){
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
  if(yaw_angle > 31 && Previous_angle > yaw_angle && start_state == 0){
    start_state = 1;
    clutch_direction = 1;
  }
  if(number_matrix < matrix_number && start_state == 1){
    static int start_time = millis();
    // degree_matrix[number_matrix] = yaw_angle;
    speed_matrix[number_matrix] = yaw_speed;
    // stage_matrix[number_matrix] = clutch_state;
    time_matrix[number_matrix] = millis() - start_time;
    number_matrix++;
  }
  Previous_angle = yaw_angle;
}


/*
 * @brief: the IRQ Handler for key
 * @return: nothing
 */
void Key_IRQHandler()  
{
  key_state = 1;
}

void setup() {
  delay(100); // Wait for sensors to get ready

  Serial.begin(115200);
  Wire.begin();
  Serial.print("**** The System Initialize... ****\n");
  IMU::init();  //Init the MPU6050

  HMC5883L::setmode_continuous();// Configure device for continuous mode
  HMC5883L::calibrate(); //calibrate the HMC
  
  /* Set Kalman and gyro starting angle */
  IMU::getdata();
  HMC5883L::getdata();
  
  IMU::updatePitchRoll();
  IMU::updateYaw();
  IMU::Kalmaninitialize();

  pinMode(button_pin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button_pin),Key_IRQHandler, FALLING);

  Timer1.initialize(10000); // 初始化 Timer1 ，定时器每间隔 10ms（10000us = 10ms）执行中断函数一次
  Timer1.attachInterrupt(Timer1_IRQHandler);

  Serial.print("**** The System Init Done... ****\n");
}

void loop() {

  IMU::InvertEulerangle();
  yaw_angle = IMU::compAngleZ - 68;
  yaw_speed = -IMU::gyroZrate;
  Key_function();
  SpeedCluthingmethod();
  /* Print Data */

  if(clutch_state == 1){
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 100){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0);
    }
  }
#if 1
  Serial.print("90 degree:");Serial.println(90);
  Serial.print("-90 degree:");Serial.println(-90);
  Serial.print("YAW_Degree:");Serial.println(yaw_angle);
  Serial.print("YAW_Speed:");Serial.println(yaw_speed);
#endif
}

