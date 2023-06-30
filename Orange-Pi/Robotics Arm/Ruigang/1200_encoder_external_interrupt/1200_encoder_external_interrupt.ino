#include "TimerOne.h"

#define matrix_number 250
#define encoderA_pin 2
#define encoderB_pin 3


/***** AB encoder variable *****/
volatile float pulse = 0; //记录A脉冲的次数
float motion = 0; //定义位移
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; //方向
float velocity=0; //速度
/******************************/

/***** clutching variable *****/
float premotion = 0;
char clutch_state = 0;
char direction = 0;
unsigned char clutch_timecount = 0;
char speed_detect_state = 0;
/******************************/

/***** time evaluation variable *****/
unsigned long timecnt = 0;
/******************************/

/***** matrix for data variable *****/
float degree_matrix[matrix_number] = {};
float speed_matrix[matrix_number] = {};
unsigned long time_matrix[matrix_number] = {};
// float clutch_matrix[matrix_number] = {};
int number_matrix = 0;
char stage_save = 0;
char send_out = 0;
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
}
   

float cal_speed(float n) //转速计算函数
{ 
  float vel = n / ((float)(micros() - timecnt) * 0.0012);   // 1200 * time * 0.001 * 0.001

  timecnt = micros(); 
  
  return vel;
}
bool store = false;
void cal_info()  //得出角度
{

  velocity = cal_speed(pulse); //计算转速

  if(current_direction == forward_direction){
    motion = motion + pulse * 360 / 1200; //计算正位移
  }
  else{
    motion = motion - pulse * 360 / 1200; //计算负位移
    velocity = -velocity;
  }
  
  pulse = 0;    //脉冲A计数归0
  store = !store;
  if(number_matrix < matrix_number && stage_save == 1 && store){
    static unsigned int matrix_time_start = millis(); //初始化一次
    degree_matrix[number_matrix] = motion;
    speed_matrix[number_matrix] = velocity;
    time_matrix[number_matrix] = millis() - matrix_time_start ;
    number_matrix++;
    // Serial.print(number_matrix);Serial.print("\n");
  }
  premotion = motion; 

}

/*
 * @brief: clutch the stick if the speed achieves the interval
           direction == 0: anticlockwise
           direction == 1: clockwise
 * @return: nothing
 */
void speed_clutch_method(){
  if(premotion < motion && clutch_state == 0 && direction == 0 && speed_detect_state ==0 && motion < -25){   //anticlockwise
    speed_detect_state = 1;
    stage_save = 1;
    direction = 1;
  }

  if(speed_detect_state == 1){
    if(velocity < 0.1 && velocity > 0 && clutch_state == 0 && direction == 1 && motion > 0){
      clutch_state = 1;
      direction = 0; 
    }
    if(velocity > -0.1 && velocity < 0  && clutch_state == 0 && direction == 0 && motion < 0){
      clutch_state = 1;
      direction = 1; 
    }
  }

}

/*
 * @brief: main funtcion
 * @return: nothing
 */
void setup(){
  delay(100);
  Serial.begin(115200);
  Serial.print("**** Start To Init The System... ****\n");

  attachInterrupt(digitalPinToInterrupt(encoderA_pin),CountA, FALLING);//中断源为0，对应着2号引脚。检测脉冲下降沿中断，并转到CountA函数

  Timer1.initialize(10000); // 初始化 Timer1 ，定时器每间隔 10ms（10000us = 10ms）执行中断函数一次
  Timer1.attachInterrupt(Timer1_IRQHandler);

  Serial.print("**** The System Init Done...     ****\n");
}

/*
 * @brief: looping
 * @return: nothing
 */
void loop() {
  speed_clutch_method();

  if(clutch_state == 1){
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 100){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0);
    }
  }
  // Serial.println("Degree:");
  // Serial.println(motion);
  // Serial.print("\n");

  // Serial.println("Speed:");
  // Serial.println(velocity);
  // Serial.print("\n");

  //超出数组的容量后触发发送函数
  if(number_matrix == matrix_number && send_out == 0){
    noInterrupts();

    Serial.print("angle = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(degree_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");
    Serial.print("velocity = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(speed_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");
    Serial.print("time = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(time_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");
    // Serial.print("clutch = np.array([");
    // for (int i = 0; i < number_matrix; i++) {
    //   Serial.print(clutch_matrix[i]);
    //   Serial.print(", ");
    // }
    // Serial.print("])\n");
    Serial.print("over");
    send_out = 1;

    interrupts();
  }
}

/*
 * @brief: Detect the AB phase encoder
 * @return: nothing
 */
void CountA()
{
  if(digitalRead(encoderB_pin) == HIGH){  //B脉冲为高电平
    current_direction = forward_direction;
  }
  else{
    current_direction = back_direction;
  }
  pulse++;
  cal_info();
}
