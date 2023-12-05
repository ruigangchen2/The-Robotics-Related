#include "TimerOne.h"

#define matrix_number 620
#define encoderA_pin 2
#define encoderB_pin 3

struct _1_ekf_filter
{
	float LastP;	
	float	Now_P;	//测量不确定性
	float out;
	float Kg;		//卡尔曼增益
	float Q;	//过程噪声的方差
	float R;	//估计不确定性
}; 

void kalman_1(struct _1_ekf_filter *ekf,float input)  //一维卡尔曼
{
	ekf->Now_P = ekf->LastP + ekf->Q;   								//p(x,x-1) = p(x-1,x-1) + Q   更新外推不确定性
	
	ekf->Kg = ekf->Now_P / (ekf->Now_P + ekf->R);				//K = p / (p + R)   更新卡尔曼增益，
	
	ekf->out = ekf->out + ekf->Kg * (input - ekf->out); //卡尔曼状态更新方程
	
	ekf->LastP = (1-ekf->Kg) * ekf->Now_P ;							//估计不确定性更新
}
// static struct _1_ekf_filter Kalman_parameter = {0.02,0,0,0,0.03,0.4};
static struct _1_ekf_filter Kalman_parameter = {0.05,0,0,0,0.065,0.53};


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
int clutch_state = 0;
char direction = 0;
int clutch_timecount = 0;
int speed_detect_state = 0;
/******************************/

/***** matrix for data variable *****/
float degree_matrix[matrix_number] = {};
float speed_matrix[matrix_number] = {};
float time_matrix[matrix_number] = {};
float clutch_matrix[matrix_number] = {};
int number_matrix = 0;
int stage_save = 0;
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
  noInterrupts();
  get_info();
  interrupts();
}
   

float cal_speed(float n) //转速计算函数
{ 
  float vel = n * 60.0 ;   //   n / (5 * 0.001 * 1200) * 360
  return vel;
}

void get_info()  //得出角度
{

  velocity = cal_speed(pulse); //计算转速
  // kalman_1(&Kalman_parameter,velocity);
  // velocity = Kalman_parameter.out;

  if(current_direction == forward_direction){
    motion = motion + pulse * 360 / 1200; //计算正位移
  }
  else{
    motion = motion - pulse * 360 / 1200; //计算负位移
    velocity = -velocity;
  }
  pulse = 0;    //脉冲A计数归0
  
  if(number_matrix < matrix_number && stage_save == 1){
    static int matrix_time_start = millis(); //初始化一次
    degree_matrix[number_matrix] = motion;
    speed_matrix[number_matrix] = velocity;
    time_matrix[number_matrix] = millis() - matrix_time_start ;
    // clutch_matrix[number_matrix] = clutch_state;
    number_matrix++;
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
  if(premotion < motion && clutch_state == 0 && direction == 0 && speed_detect_state ==0 && motion < -20){   //anticlockwise
    speed_detect_state = 1;
    stage_save = 1;
    direction = 1;
  }

  if(speed_detect_state == 1){
    if(velocity == 0 && clutch_state == 0 && direction == 1 && motion > 0){
      clutch_state = 1;
      direction = 0; 
    }
    // if(velocity > -200 && velocity < 0  && clutch_state == 0 && direction == 0 && motion < 0){
    //   clutch_state = 1;
    //   direction = 1; 
    // }
  }
}

/*
 * @brief: main funtcion
 * @return: nothing
 */
void setup(){
  Serial.begin(115200);
  Serial.print("**** Start To Init The System... ****\n");

  attachInterrupt(digitalPinToInterrupt(encoderA_pin),CountA, FALLING);//中断源为0，对应着2号引脚。检测脉冲下降沿中断，并转到CountA函数

  Timer1.initialize(5000); // 初始化 Timer1 ，定时器每间隔 5ms（5000us = 5ms）执行中断函数一次
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
    if(clutch_timecount == 50){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0);
    }
  }
  // Serial.print("Degree:");Serial.println(motion);
  // Serial.print("Speed:");Serial.println(velocity);
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
}
