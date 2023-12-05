#include <MsTimer2.h>  //定时器2
#include "TimerOne.h"

// Define constants
#define button 7
#define save_number 400

// button
bool current_state = 0;
bool previous_state = 0;
int delay_flag = 0;
int buttonstate = 0;
int count = 0;

//AB encoder
int pinA = 2;             // 定义2号端口为A脉冲输入端口
int pinB = 3;             // 定义3号端口为B脉冲输入端口
volatile float ppsA = 0;  //记录A脉冲的次数
float angle = 1;          //定义位移
float angle_save = -angle;
char a = '+';
char b = '-';
char c = 0;          //方向
float velocity = 0;  //速度

//clutching initialize
float premotion = 0;
int clutch_state = 0;
char direction = 0;
int clutch_timecount = 0;

// time evaluation
unsigned int timecnt = 0;
unsigned int current_time = 0;
unsigned int previous_time = 0;

//matrix for data
float degree_matrix[save_number] = {};
float speed_matrix[save_number] = {};
float time_matrix[save_number] = {};
float clutch_matrix[save_number] = {};
int number_matrix = 0;
int matrix_time_start = 0;
int time_stage = 0;
int stage_save = 0;

//task procedure
typedef struct {
  u8 check_flag;
  u16 err_flag;
  u8 cnt_2ms;
  u8 cnt_50ms;
} loop_t;
loop_t loop_t1;

// Timer interrupt
void Timer_interrupt()  //中断处理函数，改变灯的状态
{
  loop_t1.cnt_2ms++;
  loop_t1.cnt_50ms++;
  if (loop_t1.check_flag >= 1) {
    loop_t1.err_flag++;  // 2ms
  } else {
    loop_t1.check_flag += 1;  //该标志位在循环后面清0
  }
}

//for key
u8 KEY_Scan(u8 mode) {
  static u8 key_up = 1;  //按键按松开标志
  if (mode) key_up = 1;  //支持连按
  if (key_up && buttonstate) {
    delay(10);  //去抖动
    key_up = 0;
    if (buttonstate == 1) return 1;
  } else if (buttonstate == 0) key_up = 1;
  return 0;  // 无按键按下
}

void Task_scheduler() {
  if (loop_t1.check_flag >= 1) {
    if (loop_t1.cnt_2ms >= 1) {
      loop_t1.cnt_2ms = 0;
      Duty_2ms();  //周期2ms的任务
    }
    if (loop_t1.cnt_50ms >= 25) {
      loop_t1.cnt_50ms = 0;
      Duty_50ms();  //周期50ms的任务
    }
    loop_t1.check_flag = 0;  //循环运行完毕标志
  }
}

/////////////////////////////////////////////////////////////
void Duty_2ms() {
  delay_flag++;
}

//////////////////////////////////////////////////////////
void Duty_50ms()  //for the key task
{
  if (clutch_state == 1) {  //count the number and replace the delay()
    ++clutch_timecount;
  }
  buttonstate = digitalRead(button);
  if (KEY_Scan(0) == 1) {
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
  }
}

void read_velocity()  //得出角度
{
  int w = ppsA;
  float temp = 0;
  velocity = float(w) * 0.9 / ((millis() - timecnt) * 0.001);
  timecnt = millis();
  if (c == a) {
    temp = ppsA * 360 / 400;  //计算正位移
  } else {
    temp =  - ppsA * 360 / 400;  //计算负位移
  }
  angle = angle + temp;
  ppsA = 0;  //脉冲A计数归0

  current_state = temp>0;
  if (delay_flag >= 50){
    if (current_state != previous_state){
      clutch_state = 1;
    }
    delay_flag = 0; // there is 10*10ms delay
  }
  previous_state = current_state;

  if (number_matrix < save_number) {
    if (time_stage == 0) {
      matrix_time_start = millis();
      time_stage = 1;
    }
    degree_matrix[number_matrix] = angle;
    speed_matrix[number_matrix] = current_state;
    time_matrix[number_matrix] = millis() - matrix_time_start;
    clutch_matrix[number_matrix] = clutch_state;
    number_matrix++;
  }
}

void setup() {
  delay(500);
  Serial.begin(9600);
  Serial.print("Start To Init The System...\n");
  Serial.print("--------------------\n");

  attachInterrupt(0, CountA, CHANGE);  //中断源为0，对应着2号引脚。检测脉冲下降沿中断，并转到CountA函数
  attachInterrupt(1, CountB, CHANGE);  //中断源为1，对应着3号引脚。检测脉冲下降沿中断，并转到CountA函数

  pinMode(button, INPUT_PULLUP);

  MsTimer2::set(2, Timer_interrupt);  // 中断设置函数，每 2ms 进入一次中断
  MsTimer2::start();                  //开始计时
  Serial.print("The System Init Done\n");
  Serial.print("--------------------\n");
}


void loop() {
  Task_scheduler();
  if (clutch_state == 1) {
    digitalWrite(5, 1);            // 100% PWM wave
    if (clutch_timecount == 20) {  //replace the delay function.
      clutch_timecount = 0;
      clutch_state = 0;
      digitalWrite(5, 0);
      delay(30);
    }
  }
}



// 四倍频
void CountA() {
  if (digitalRead(pinA) == HIGH) {  //B脉冲为高电平
    if (digitalRead(pinB) == HIGH) {
      c = a;
      ppsA++;
    } else {
      ppsA--;
    }
  } else {
    if (digitalRead(pinB) == LOW) {
      c = a;
      ppsA++;
    } else {
      ppsA--;
    }
  }
  read_velocity();
}
void CountB() {
  if (digitalRead(pinB) == HIGH) {  //B脉冲为高电平
    if (digitalRead(pinA) == LOW) {
      c = a;
      ppsA++;
    } else {
      ppsA--;
    }
  } else {
    if (digitalRead(pinA) == HIGH) {
      c = a;
      ppsA++;
    } else {
      ppsA--;
    }
  }
  read_velocity();
}