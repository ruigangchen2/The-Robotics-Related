#include <MsTimer2.h>        //定时器2
#include "TimerOne.h"

#define matrix_number 480
#define button_pin 18
#define encoderA_pin 2
#define encoderB_pin 3

/***** button variable *****/
char count = 0;
char key_state = 0;
/******************************/

/***** AB encoder variable *****/
volatile float pulse = 0; //记录A脉冲的次数
float motion = 0; //定义位移
char forward_direction = '+';
char current_direction = 0; //方向
float velocity=0; //速度
/******************************/

/***** clutching variable *****/
float premotion = 0;
int clutch_state = 0;
char direction = 0;
int clutch_timecount = 0;
int speed_detect_state = 0;
/******************************/

/***** time evaluation variable *****/
unsigned int timecnt = 0;
/******************************/

/***** matrix for data variable *****/
float degree_matrix[matrix_number] = {};
float speed_matrix[matrix_number] = {};
float time_matrix[matrix_number] = {};
float clutch_matrix[matrix_number] = {};
int number_matrix = 0;
int stage_save = 0;
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


/*
 * @brief: the key function for key
 * @return: nothing
 */
void Key_function()  
{
  if(key_state == 1){
    delay(5);
    if(digitalRead(button_pin)){
      ++count;
      key_state = 0;
    }
  }

  switch(count){
  case 2:  //If you want to send the matrix data, just click the key twice.
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
    Serial.print("clutch = np.array([");
    for (int i = 0; i < number_matrix; i++) {
      Serial.print(clutch_matrix[i]);
      Serial.print(", ");
    }
    Serial.print("])\n");
    count++;
    break;  
  case 3:
    count = 0;
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


float cal_speed(float n) //转速计算函数
{ 
  float vel = n * 0.9 / ((millis() - timecnt) * 0.001); 
  timecnt = millis(); 
  return vel;
}


void cal_degree()  //得出角度
{
  int w = motion;

  noInterrupts();
  
  velocity = cal_speed(w); //计算转速

  if(current_direction == forward_direction){
    motion = motion + motion * 360 / 400; //计算正位移
  }
  else{
    motion = motion - motion * 360 / 400; //计算负位移
  }
  motion = 0;    //脉冲A计数归0
  
  interrupts();
  if(number_matrix < 500 && stage_save == 1){
    static int matrix_time_start = millis(); //初始化一次
    degree_matrix[number_matrix] = motion;
    speed_matrix[number_matrix] = velocity;
    time_matrix[number_matrix] = millis() - matrix_time_start ;
    number_matrix++;
  }
}

/*
 * @brief: clutch the stick if the speed achieves the interval
           direction == 0: anticlockwise
           direction == 1: clockwise
 * @return: nothing
 */
void speed_clutch_method(){
  if(premotion > motion && clutch_state == 0 && direction == 0 && speed_detect_state ==0){   //anticlockwise
    speed_detect_state = 1;
    stage_save = 1;
    direction = 1;
  }

  if(speed_detect_state == 1){
    if(velocity < 100 && velocity > 0 && clutch_state == 0 && direction == 0 && motion > 0){
      clutch_state = 1;
      direction = 1;
    }
    if(velocity > -100 && velocity < 0  && clutch_state == 0 && direction == 1 && motion < 0){
      clutch_state = 1;
      direction = 0;
    }
  }
  premotion = motion; 
}

/*
 * @brief: main funtcion
 * @return: nothing
 */
void setup(){
  delay(100);
  Serial.begin(9600);
  Serial.print("**** Start To Init The System... ****\n");

  attachInterrupt(digitalPinToInterrupt(encoderA_pin),CountA, CHANGE);//中断源为0，对应着2号引脚。检测脉冲下降沿中断，并转到CountA函数
  attachInterrupt(digitalPinToInterrupt(encoderB_pin),CountB, CHANGE);//中断源为1，对应着3号引脚。检测脉冲下降沿中断，并转到CountA函数

  pinMode(button_pin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button_pin),Key_IRQHandler, FALLING);

  // MsTimer2::set(2, Timer_interrupt);        // 中断设置函数，每 2ms 进入一次中断
  // MsTimer2::start();                //开始计时

  Timer1.initialize(10000); // 初始化 Timer1 ，定时器每间隔 10ms（10000us = 10ms）执行中断函数一次
  Timer1.attachInterrupt(Timer1_IRQHandler);

  Serial.print("**** The System Init Done...     ****\n");
}

/*
 * @brief: looping
 * @return: nothing
 */
void loop() {
  
  Key_function();
  speed_clutch_method();

  if(clutch_state == 1){
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 100){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0);
    }
  }
}


/*
 * @brief: Detect the AB phase encoder
 * @return: nothing
 */
void CountA()
{
  if(digitalRead(encoderA_pin) == HIGH){ //B脉冲为高电平
    if(digitalRead(encoderB_pin) == HIGH){
      current_direction = forward_direction;
      motion++;
    }
    else{
      motion--;
    }
  }
  else{
    if(digitalRead(encoderB_pin) == LOW){
      current_direction = forward_direction;
      motion++;
    }
    else{
      motion--;
    }
  }
  cal_degree();
}

void CountB()
{
  if(digitalRead(encoderB_pin) == HIGH){ //B脉冲为高电平
    if(digitalRead(encoderA_pin) == LOW){
      current_direction = forward_direction;
      motion++;
    }
    else{
      motion--;
    }
  }
  else{
    if(digitalRead(encoderA_pin) == HIGH){
      current_direction = forward_direction;
      motion++;
    }
    else{
      motion--;
    }
  }
  cal_degree();
}