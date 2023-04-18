#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
#include <pthread.h>
#include <wiringPi.h>
#include <sys/time.h>
#include <signal.h>

/*
gcc -o robotic_armV3_0 robotic_armV3_0.c -lwiringPi -pthread -lcrypt -lm -lrt
*/

#define encoderA_pin 4
#define encoderB_pin 5
#define electromagnet_1 9
#define electromagnet_2 10
#define electromagnet_3 9
#define electromagnet_4 10


/***** AB encoder variable *****/
float pulse = 0; //记录A脉冲的次敄1�7
float motion = 0; //定义位移
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; //方向
char direction_state = 0;
float velocity=0; //速度
/******************************/

/***** Testing time *****/
double TimeUse=0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

/***** File  *****/
static volatile int file_state = 1;
/******************************/


void cal_info() 
{
    velocity = pulse * 48.0; //   n / (0.005 * 1500) * 360

    if(current_direction == forward_direction){
        motion = motion + pulse * 360 / 1500;
    }
    else{
        motion = motion - pulse * 360 / 1500; 
        velocity = -velocity;
    }
    pulse = 0;   
    printf("motion is:%.2f\n",motion);
}


void IRQ_APhase(void)
{
  if(digitalRead(encoderB_pin) == HIGH){  //B脉冲为高电平
    current_direction = forward_direction;
  }
  else{
    current_direction = back_direction;
  }
  pulse++;
}


void testingT_start()
{
    gettimeofday(&StartTime, NULL); 
}

double testingT_end()
{
    gettimeofday(&EndTime, NULL);   //测量结束
    TimeUse = 1000000*(EndTime.tv_sec-StartTime.tv_sec)+EndTime.tv_usec-StartTime.tv_usec;
    TimeUse/=1000;  //测量结果，毫秒级
    return TimeUse;
}

void intHandler(int i)
{
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    file_state = 0;
}

void *Timer_5ms(void)
{   
    testingT_start();

    FILE *fp = fopen("./robotic_arm.csv", "w+");
    if (fp == NULL) {
        fprintf(stderr, "fopen() failed.\n");
        printf("Failed\n");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Time,Degree,Velocity\n");
    signal(SIGINT, intHandler);
    while(1){
        cal_info();

        if(file_state == 1)
            fprintf(fp,"%.2f,%.2f,%.2f\n",testingT_end(),motion,velocity);
        else
            fclose(fp); 
        delay(5);
    }
}

int main(int argc, const char *argv[])
{
    pthread_t id1;
	int value;

    wiringPiSetup();
    pinMode(encoderA_pin, INPUT);
    pullUpDnControl (encoderA_pin, PUD_UP);
    delay(100);
    wiringPiISR(encoderA_pin,INT_EDGE_FALLING,&IRQ_APhase);


    value = pthread_create(&id1, NULL, (void *)Timer_5ms, NULL);
	if(value){
        printf("thread1 is not created!\n");
        return -1;
	}
    printf("All the thread is created..\n");
    
    pthread_join(id1,NULL);
	return 0;
}

