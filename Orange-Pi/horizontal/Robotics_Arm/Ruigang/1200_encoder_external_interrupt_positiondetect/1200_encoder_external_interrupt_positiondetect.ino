#include "TimerOne.h"

#define matrix_number 950
#define encoderA_pin 2
#define encoderB_pin 3
#define button_pin 18

/***** button variable *****/
char key_count = 0;
char key_state = 0;
/******************************/

/***** AB encoder variable *****/
volatile float pulse = 0; //记录A脉冲的次数
float motion = 0; //定义位移
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; //方向
/******************************/

/***** clutching variable *****/
float premotion = 0;
char clutch_state = 0;
char direction = 0;
unsigned char clutch_timecount = 0;
char position_detect_state = 0;
/******************************/

/***** time evaluation variable *****/
unsigned long timecnt = 0;
/******************************/

/***** matrix for data variable *****/
float degree_matrix[matrix_number] = {};
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


void cal_info()  //得出角度
{

  if(current_direction == forward_direction){
    motion = motion + pulse * 360 / 1200; //计算正位移
  }
  else{
    motion = motion - pulse * 360 / 1200; //计算负位移
  }
  
  pulse = 0;    //脉冲A计数归0

  position_clutch_method();

  if(number_matrix < matrix_number && stage_save == 1){
    static unsigned int matrix_time_start = millis(); //初始化一次
    degree_matrix[number_matrix] = motion;
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
void position_clutch_method(){
  if(premotion < motion && clutch_state == 0 && direction == 0 && position_detect_state ==0 && motion < -25){   //anticlockwise
    position_detect_state = 1;
    stage_save = 1;
    direction = 1;
  }

  if(position_detect_state == 1){
    if(premotion > motion && clutch_state == 0 && direction == 1 && motion > 0){
      clutch_state = 1;
      direction = 0; 
    }
    if(premotion < motion  && clutch_state == 0 && direction == 0 && motion < 0){
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

  pinMode(button_pin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(button_pin),Key_IRQHandler, FALLING);

  Timer1.initialize(10000); // 初始化 Timer1 ，定时器每间隔 10ms（10000us = 10ms）执行中断函数一次
  Timer1.attachInterrupt(Timer1_IRQHandler);

  Serial.print("**** The System Init Done...     ****\n");
}

/*
 * @brief: looping
 * @return: nothing
 */
void loop() {
  // position_clutch_method();
  Key_function();

  if(clutch_state == 1){
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 20){  //replace the delay function.
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
