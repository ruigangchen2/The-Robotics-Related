#include <MsTimer2.h>        //定时器2
#include <TimerOne.h>       //定时器1
#define button 7

// button
int buttonstate = 0;
int count = 0;
//AB encoder
int pinA=2; // 定义2号端口为A脉冲输入端口
int pinB=3;// 定义3号端口为B脉冲输入端口
volatile float ppsA=0; //记录A脉冲的次数
float m=0; //定义位移
char a='+';
char b='-';
char c = 0; //方向
float velocity=0; //速度

//clutching initialize
float premotion = 0;
char clutch_state = 0;
char direction = 0;
int clutch_timecount = 0;

// time evaluation
unsigned int timecnt = 0;

//matrix for data
float clutchmatrix[800] = {};
float timematrix[800] = {};

int number_matrix = 0;
int time_stage = 0;
int stage_save = 0;
int speed_detect_state = 0;


//task procedure
typedef struct{
  u8 check_flag;
  u16 err_flag;
  u8 cnt_2ms;
  u8 cnt_4ms;
  u8 cnt_6ms;
  u8 cnt_10ms;
  u8 cnt_20ms;
  u8 cnt_50ms;
  u16 cnt_1000ms;
}loop_t;
loop_t loop_t1;

void Timer_interrupt()          //中断处理函数，改变灯的状态
{ 
  loop_t1.cnt_2ms++;
  loop_t1.cnt_4ms++;
  loop_t1.cnt_6ms++;
  loop_t1.cnt_10ms++;
  loop_t1.cnt_20ms++;
  loop_t1.cnt_50ms++;
  loop_t1.cnt_1000ms++;

  if( loop_t1.check_flag >= 1){
    loop_t1.err_flag ++;  // 2ms
  }
  else{
    loop_t1.check_flag += 1;   //该标志位在循环后面清0
  }
}

//for key
u8 KEY_Scan(u8 mode)
{	 
	static u8 key_up=1;//按键按松开标志
	if(mode)key_up=1;  //支持连按		  
	if(key_up && buttonstate)
	{
		delay(10);//去抖动 
		key_up=0;
	  if(buttonstate == 1)return 1;
		
	}else if(buttonstate == 0)key_up=1; 	    
 	return 0;// 无按键按下
}


void Task_scheduler()
{
    if( loop_t1.check_flag >= 1 )
    {
    if( loop_t1.cnt_2ms >= 1 )
    {
      loop_t1.cnt_2ms = 0;
      Duty_2ms();           //周期2ms的任务
    }
    if( loop_t1.cnt_4ms >= 2 )
    {
      loop_t1.cnt_4ms = 0;
      Duty_4ms();           //周期4ms的任务
    }
    if( loop_t1.cnt_6ms >= 3 )
    {
      loop_t1.cnt_6ms = 0;
      Duty_6ms();           //周期6ms的任务
    }
    if( loop_t1.cnt_10ms >= 5 )
    {
      loop_t1.cnt_10ms = 0;
      Duty_10ms();          //周期10ms的任务
    } 
    if( loop_t1.cnt_20ms >= 10 )
    {
      loop_t1.cnt_20ms = 0;
      Duty_20ms();          //周期20ms的任务
    }
    if( loop_t1.cnt_50ms >= 25 )
    {
      loop_t1.cnt_50ms = 0;
      Duty_50ms();          //周期50ms的任务
    }
    if( loop_t1.cnt_1000ms >= 500)
    {
      loop_t1.cnt_1000ms = 0;
      Duty_1000ms();        //周期1s的任务
    }
     loop_t1.check_flag = 0;        //循环运行完毕标志
    }
}

/////////////////////////////////////////////////////////////
void Duty_2ms()
{
 
}
//////////////////////////////////////////////////////////

void Duty_4ms()
{
 
}
//////////////////////////////////////////////////////////
void Duty_6ms()
{

}
/////////////////////////////////////////////////////////
void Duty_10ms()
{
  if(clutch_state == 1){   //count the number and replace the delay()
    ++clutch_timecount;
  }

  
}
/////////////////////////////////////////////////////////
void Duty_20ms()  //If you want to see the figure, just don't comment
{
  
  if (velocity > 0){
    Serial.print(c);
  }
  Serial.print(velocity*10); // 将获取的数字信号值打印到串口显示
  Serial.print(" r/s  ");
  Serial.print(m);
  Serial.println("°");

}
//////////////////////////////////////////////////////////
void Duty_50ms()  //for the key task
{
  buttonstate = digitalRead(button);

  if(KEY_Scan(0) == 1)
  {
    Serial.print("press down\n");
    ++count;
  }

  switch(count){
  case 1:

    break;
  case 2:  //If you want to send the matrix data, just click the key twice.
    Serial.print("Start sending\n");
    for(int i = 0; i < number_matrix; i++){  
      Serial.print(clutchmatrix[i]);
      Serial.print(" ");
    }
    Serial.print("\n");
    for(int i = 0; i < number_matrix; i++){  
      Serial.print(timematrix[i]);
      Serial.print(" ");
    }
    Serial.print("\n");
    Serial.print("Finished sending\n");
    count++;
    break;  
  case 3:
    count = 0;
    break;      
  default:
    break;
  }

}
/////////////////////////////////////////////////////////////
// for the time evaluation
int examplenumber = 0;
void Duty_1000ms()
{

    // examplenumber++;
    // Serial.print("examplenumber= ");
    // Serial.print(examplenumber);
    // Serial.print("\n");
    // if(examplenumber == 100){
    // examplenumber = 0;
    // Serial.print("timecnt= ");
    // Serial.print(millis() - timecnt);
    // Serial.print("\n");
}
/////////////////////////////////;////////////////////////////

float v(float n) //转速计算函数
{
  float vel = n/40; // n/(100*4*0.1)
  return vel;
}

void flash()  //得出角度
{
  int w = ppsA;

  noInterrupts();
  
  velocity = v(w); //计算转速
  if(c == a){
    m = m + ppsA * 360 / 400; //计算正位移
  }
  else{
    m = m - ppsA * 360 / 400; //计算负位移
  }
  ppsA = 0;    //脉冲A计数归0

  if(number_matrix < 800 && speed_detect_state == 1){
    if(time_stage == 0){
      timecnt = millis();
      time_stage = 1;
    }
    clutchmatrix[number_matrix] = m;
    timematrix[number_matrix] = millis() - timecnt;
    number_matrix++;
    }
  interrupts();

  
}

void setup(){
  delay(500);
  Serial.begin(9600);
  Serial.print("Start To Init The System...\n");
  Serial.print("--------------------\n");

  attachInterrupt(0,CountA, CHANGE);//中断源为0，对应着2号引脚。检测脉冲下降沿中断，并转到CountA函数
  attachInterrupt(1,CountB, CHANGE);//中断源为1，对应着3号引脚。检测脉冲下降沿中断，并转到CountA函数

  pinMode(button,INPUT_PULLUP);

  MsTimer2::set(2, Timer_interrupt);        // 中断设置函数，每 2ms 进入一次中断
  MsTimer2::start();                //开始计时

  Timer1.initialize(100000); // 初始化 Timer1
  Timer1.attachInterrupt(flash); // 设定 flash 为 Timer 的中断函数

  Serial.print("The System Init Done\n");
  Serial.print("--------------------\n");

}

void degree_clutch_method(){

  if(premotion > m && clutch_state == 0 && direction == 0){   //anticlockwise
    clutch_state = 1;
    direction = 1; //逆时针转
    stage_save = 1;
  }
  if(premotion < m && clutch_state == 0 && direction == 1){ //clockwise
    clutch_state = 1;
    direction = 0; //顺时针转
    stage_save = 1;
  }
  premotion = m; 

}


void speed_clutch_method(){
  if(premotion > m && clutch_state == 0 && direction == 0 && speed_detect_state == 0){   //anticlockwise
    speed_detect_state = 1;
  }
  if(speed_detect_state){
  if(velocity*10 < 50 && velocity*10 > 0  && clutch_state == 0 && direction == 0){
    clutch_state = 1;
    direction = 1; //逆时针转
    stage_save = 1;
  }
  if(velocity*10 > -50 && velocity*10 < 0 && clutch_state == 0 && direction == 1){
    clutch_state = 1;
    direction = 0; //逆时针转
    stage_save = 1;
  }
  }
  if(speed_detect_state == 0)premotion = m; 
}

void loop() {
  
  Task_scheduler();
  
  // degree_clutch_method();
  speed_clutch_method();

  if(clutch_state == 1){
    
    analogWrite(5,255); // 100% PWM wave
    if(clutch_timecount == 100){  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      analogWrite(5,0); 
    }
  }
  
/********* if you want to use the data matrix, just don't comment it *************/
  // if(number_matrix < 800 && premotion != m){ 
  // if(number_matrix < 800 && stage_save == 1){
  //   if(time_stage == 0){
  //     timecnt = millis();
  //     matrix_time_state = 1;
  //     time_stage = 1;
  //   }
  //   if(matrix_time == 1){
  //   matrix_time = 0;
  //   clutchmatrix[number_matrix] = m;
  //   timematrix[number_matrix] = millis() - timecnt;
  //   number_matrix++;
  //   }
  // }
/********************************************************************************/   
  
}


//四倍频
void CountA()
{
  if(digitalRead(pinA) == HIGH){ //B脉冲为高电平
    if(digitalRead(pinB) == HIGH){
      c=a;
      ppsA++;
    }
    else{
      ppsA--;
    }
  }
  else{
    if(digitalRead(pinB) == LOW){
      c=a;
      ppsA++;
    }
    else{
      ppsA--;
    }
  }
}

void CountB()
{
  if(digitalRead(pinB) == HIGH){ //B脉冲为高电平
    if(digitalRead(pinA) == LOW){
      c=a;
      ppsA++;
    }
    else{
      ppsA--;
    }
  }
  else{
    if(digitalRead(pinA) == HIGH){
      c=a;
      ppsA++;
    }
    else{
      ppsA--;
    }
  }
}

