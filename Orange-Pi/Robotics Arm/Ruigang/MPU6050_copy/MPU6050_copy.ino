#include <MsTimer2.h>               //定时器库的 头文件
#include <Wire.h>
#include <math.h>


int16_t MpuOffset[6] = {0};//MPU6050 6 参数
const int MPU = 0x68; // MPU6050 I2C address
const float RtA = 57.2957795f;//180/pi
const float Gyro_G = 0.03051756f*2;     
const float Gyro_Gr = 0.0005326f*2;   

#define squa( Sq )        (((float)Sq)*((float)Sq))//squa


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

typedef struct{     //定义结构，6个参数
  int16_t accX;
  int16_t accY;
  int16_t accZ;
  int16_t gyroX;
  int16_t gyroY;
  int16_t gyroZ;
}_st_Mpu;
_st_Mpu MPU6050; 

typedef struct{     //定义结构体
  float roll; //横滚角
  float pitch; //俯仰角
  float yaw; //偏航角
}_st_AngE;
_st_AngE Angle; 

typedef volatile struct {  //四元数结构体
  float q0;
  float q1;
  float q2;
  float q3;
} Quaternion;

struct _1_ekf_filter  //卡尔曼滤波结构体
{
  float LastP;  
  float Now_P; 
  float out;
  float Kg;   
  float Q;  
  float R;  
};



/************************/

float Q_rsqrt(float number)// 1/root(x)
{
  long i;
  float x2, y;
  const float threehalfs = 1.5F;
 
  x2 = number * 0.5F;
  y  = number;
  i  = * ( long * ) &y;                      
  i  = 0x5f3759df - ( i >> 1 );               
  y  = * ( float * ) &i;
  y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration （第一次牛顿迭代）
  return y;
} 

void GetAngle(const _st_Mpu *pMpu,_st_AngE *pAngE, float dt) //计算角度
{    
  volatile struct V{
        float x;
        float y;
        float z;
        } Gravity,Acc,Gyro,AccGravity;

  static struct V GyroIntegError = {0};
  static  float KpDef = 0.08f ;
  static  float KiDef = 0.0003f;
  static Quaternion NumQ = {1, 0, 0, 0};   
  float q0_t,q1_t,q2_t,q3_t;
  float NormQuat; 
  float HalfTime = dt * 0.5f;
 
  NormQuat = Q_rsqrt(squa(MPU6050.accX)+ squa(MPU6050.accY) +squa(MPU6050.accZ));//normalized

  Acc.x = pMpu->accX * NormQuat;
  Acc.y = pMpu->accY * NormQuat;
  Acc.z = pMpu->accZ * NormQuat;  
  
  Gravity.x = 2*(NumQ.q1 * NumQ.q3 - NumQ.q0 * NumQ.q2);                
  Gravity.y = 2*(NumQ.q0 * NumQ.q1 + NumQ.q2 * NumQ.q3);              
  Gravity.z = 1-2*(NumQ.q1 * NumQ.q1 + NumQ.q2 * NumQ.q2);  
  
  AccGravity.x = (Acc.y * Gravity.z - Acc.z * Gravity.y);
  AccGravity.y = (Acc.z * Gravity.x - Acc.x * Gravity.z);
  AccGravity.z = (Acc.x * Gravity.y - Acc.y * Gravity.x);
  
  GyroIntegError.x += AccGravity.x * KiDef;
  GyroIntegError.y += AccGravity.y * KiDef;
  GyroIntegError.z += AccGravity.z * KiDef;

  Gyro.x = pMpu->gyroX * Gyro_Gr + KpDef * AccGravity.x  +  GyroIntegError.x; 
  Gyro.y = pMpu->gyroY * Gyro_Gr + KpDef * AccGravity.y  +  GyroIntegError.y;
  Gyro.z = pMpu->gyroZ * Gyro_Gr + KpDef * AccGravity.z  +  GyroIntegError.z;   

 
  q0_t = (-NumQ.q1*Gyro.x - NumQ.q2*Gyro.y - NumQ.q3*Gyro.z) * HalfTime; //龙格库塔法更新四元数
  q1_t = ( NumQ.q0*Gyro.x - NumQ.q3*Gyro.y + NumQ.q2*Gyro.z) * HalfTime;
  q2_t = ( NumQ.q3*Gyro.x + NumQ.q0*Gyro.y - NumQ.q1*Gyro.z) * HalfTime;
  q3_t = (-NumQ.q2*Gyro.x + NumQ.q1*Gyro.y + NumQ.q0*Gyro.z) * HalfTime;
  NumQ.q0 += q0_t;
  NumQ.q1 += q1_t;
  NumQ.q2 += q2_t;
  NumQ.q3 += q3_t;
  
  
  NormQuat = Q_rsqrt(squa(NumQ.q0) + squa(NumQ.q1) + squa(NumQ.q2) + squa(NumQ.q3));
  NumQ.q0 *= NormQuat;
  NumQ.q1 *= NormQuat;
  NumQ.q2 *= NormQuat;
  NumQ.q3 *= NormQuat;  

  {
  float vecxZ = 2 * NumQ.q0 *NumQ.q2 - 2 * NumQ.q1 * NumQ.q3 ;
  float vecyZ = 2 * NumQ.q2 *NumQ.q3 + 2 * NumQ.q0 * NumQ.q1;
  float veczZ =  1 - 2 * NumQ.q1 *NumQ.q1 - 2 * NumQ.q2 * NumQ.q2;  
  
  float yaw_G = pMpu->gyroZ * Gyro_G;
  if((yaw_G > 1.0f) || (yaw_G < -1.0f)){
    pAngE->yaw  += yaw_G * dt;
  }
  pAngE->pitch  =  asin(vecxZ)* RtA;   
  pAngE->roll = atan2f(vecyZ,veczZ) * RtA;  
  } 
}

void kalman_1(struct _1_ekf_filter *ekf,float input)  //卡尔曼滤波
{
  ekf->Now_P = ekf->LastP + ekf->Q;                  
  
  ekf->Kg = ekf->Now_P / (ekf->Now_P + ekf->R);      
  
  ekf->out = ekf->out + ekf->Kg * (input - ekf->out); 
  
  ekf->LastP = (1-ekf->Kg) * ekf->Now_P ;           
}

static struct _1_ekf_filter Kalman_parameter[3] = {{0.02,0,0,0,0.00,0.543},{0.02,0,0,0,0.003,0.543},{0.02,0,0,0,0.003,0.543}};
                                                   
static volatile int16_t *pMpu = (int16_t *)&MPU6050; 

void MpuGetOffset(void) 
{
  int32_t buffer[6]={0};
  int16_t i;  
  uint8_t k=30;
  const int8_t MAX_GYRO_QUIET = 5;
  const int8_t MIN_GYRO_QUIET = -5; 
                                            
  int16_t LastGyro[3] = {0};
  int16_t ErrorGyro[3]; 
  
  memset(MpuOffset,0,12);

  MpuOffset[2] = 8192;   
  
  while(k--){
    do{
      delay(10);
      MpuGetData();
      for(i=0;i<3;i++){       
        ErrorGyro[i] = pMpu[i+3] - LastGyro[i];  
        LastGyro[i] = pMpu[i+3];  
      }
    }while ((ErrorGyro[0] > MAX_GYRO_QUIET )|| (ErrorGyro[0] < MIN_GYRO_QUIET)
          ||(ErrorGyro[1] > MAX_GYRO_QUIET )|| (ErrorGyro[1] < MIN_GYRO_QUIET)
          ||(ErrorGyro[2] > MAX_GYRO_QUIET )|| (ErrorGyro[2] < MIN_GYRO_QUIET)
            );

  } 

  for(i=0;i<356;i++){   
    MpuGetData();
    if(100 <= i){
      uint8_t k;
      for(k=0;k<6;k++){
        buffer[k] += pMpu[k];
      }
    }
  }
  
  for(i=0;i<6;i++){
    MpuOffset[i] = buffer[i]>>8;
  }
}

int i = 0;
void MpuGetData(void) //MPU6050得到数据
{
    Wire.beginTransmission(MPU);
    Wire.write(0x3B); // Start with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
    pMpu[0] = (Wire.read() << 8 | Wire.read()) - MpuOffset[0]; //8192
    pMpu[1] = (Wire.read() << 8 | Wire.read()) - MpuOffset[1];
    pMpu[2] = (Wire.read() << 8 | Wire.read()) - MpuOffset[2];
    
    Wire.beginTransmission(MPU);
    Wire.write(0x43); // Gyro data first register address 0x43
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 4 registers total, each axis value is stored in 2 registers
    pMpu[3] = (Wire.read() << 8 | Wire.read())  - MpuOffset[3]; //16.4
    pMpu[4] = (Wire.read() << 8 | Wire.read())  - MpuOffset[4];
    pMpu[5] = (Wire.read() << 8 | Wire.read())  - MpuOffset[5]; 
    
    for(i = 0; i < 6; i++){
      if(i<3){
        kalman_1(&Kalman_parameter[i],(float)pMpu[i]);
        pMpu[i] = (int16_t)Kalman_parameter[i].out; 
      }
      if(i>2){
        uint8_t k = i - 3;
        const float factor = 0.15f;
        static float tBuff[3];
        pMpu[i] = tBuff[k] = tBuff[k] * (1 - factor) + pMpu[i] * factor;        
      } 
    }
}


void Duty_2ms()
{ 

   MpuGetData();

}
//////////////////////////////////////////////////////////

void Duty_4ms()
{

   GetAngle(&MPU6050,&Angle,0.004f);   //更新姿态数据
   
}
//////////////////////////////////////////////////////////
void Duty_6ms()
{
  

}
/////////////////////////////////////////////////////////
void Duty_10ms()
{
 
}
/////////////////////////////////////////////////////////
void Duty_20ms()
{

}
//////////////////////////////////////////////////////////
void Duty_50ms()
{
  Serial.print("Roll:");Serial.println(Angle.roll);
}
/////////////////////////////////////////////////////////////

void Duty_1000ms()
{

}


void Timer_interrupt()          //中断处理函数，改变灯的状态
{ 
  loop_t1.cnt_2ms++;
  loop_t1.cnt_4ms++;
  loop_t1.cnt_6ms++;
  loop_t1.cnt_10ms++;
  loop_t1.cnt_20ms++;
  loop_t1.cnt_50ms++;
  loop_t1.cnt_1000ms++;
  if( loop_t1.check_flag >= 1)
{
    loop_t1.err_flag ++;// 2ms
}
else
{
    loop_t1.check_flag += 1;   //该标志位在循环后面清0
}
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

void setup() {
  
  Serial.begin(9600);
  Serial.print("Start To Init The IMU...\n");
  Wire.begin();                      // Initialize comunication
  Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
  Wire.write(0x6B);                 
  Wire.write(0x80);     //复位            
  Wire.endTransmission(true);        //end the transmission
  delay(30);

  Wire.beginTransmission(MPU); 
  Wire.write(0x19);                
  Wire.write(0x02);   //陀螺仪采样率 500HZ
  Wire.endTransmission(true); 

  Wire.beginTransmission(MPU); 
  Wire.write(0x6B);                
  Wire.write(0x03);  //设置设备时钟源，陀螺仪Z轴
  Wire.endTransmission(true); 

  Wire.beginTransmission(MPU); 
  Wire.write(0x1A);                
  Wire.write(0x03);   //低通滤波 42Hz
  Wire.endTransmission(true); 

  Wire.beginTransmission(MPU); 
  Wire.write(0x1B);                
  Wire.write(0x18); //角速度计 +-2000g/s
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU); 
  Wire.write(0x1C);                
  Wire.write(0x09); //加速度计 +-4g
  Wire.endTransmission(true);

  Serial.print("IMU Init Done...\n");
  Serial.print("Start To Correct The IMU...\n");

  MpuGetOffset();

  Serial.print("Correct Done...\n");
  Serial.print("The System Init Done\n");

  MsTimer2::set(2, Timer_interrupt);        // 中断设置函数，每 2ms 进入一次中断
  MsTimer2::start();             
}

void loop() {
  Task_scheduler();
}
