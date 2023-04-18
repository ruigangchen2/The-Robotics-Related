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
Reference:
https://zhou-yuxin.github.io/articles/2017/Linux的GPIO子系统之-sys-class-gpio目录/index.html

gcc -o Robotics_Arm_Orangepi5 Robotics_Arm_Orangepi5.c -lwiringPi -pthread -lcrypt -lm -lrt


echo 92 > /sys/class/gpio/export  # Encoder A Phase 
echo in > /sys/class/gpio/gpio92/direction
echo falling > /sys/class/gpio/gpio92/edge
*/

#define encoderB_pin 15
#define electromagnet_1 9
#define electromagnet_2 6
#define electromagnet_3 4
#define electromagnet_4 3

/***** AB encoder variable *****/
float pulse = 0;  //count the pulse of the encoder
float motion = 0; 
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; 
char direction_state = 0;
float velocity=0; 
/******************************/

/***** Testing time *****/
double TimeUse=0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

struct pollfd fds[1];

void get_info()  //calculate the information of the encoder
{
    velocity = pulse * 48.0; //   n / (5 * 0.001 * 1500) * 360

    if(current_direction == forward_direction){
        motion = motion + pulse * 360 / 1500; //calculate the positive motion 
    }
    else{
        motion = motion - pulse * 360 / 1500; //calculate the negative motion 
        velocity = -velocity;
    }
    pulse = 0;    //set pulse to zero
    printf("motion is:%.2f\n",motion);
}


void *create(void)
{
    int fd = open("/sys/class/gpio/gpio92/value",O_RDONLY);
    if(fd<0){
        perror("open '/sys/class/gpio/gpio92/value' failed!\n");  
        return (void *)-1;
    }
    fds[0].fd=fd;
    fds[0].events=POLLPRI;

    while(1){
        if(poll(fds,1,0)==-1){
            printf("poll failed!\n");
            return (void *)-1;
        }
        if(fds[0].revents&POLLPRI){
            if(lseek(fd,0,SEEK_SET)==-1){
                printf("lseek failed!\n");
                return (void *)-1;
            }
            char buffer[16];
            int len;
            if((len=read(fd,buffer,sizeof(buffer)))==-1){
                printf("read failed!\n");
                return (void *)-1;
            }
            else{
                if(digitalRead(encoderB_pin) == HIGH){  //if B pin is in the high place
                    current_direction = forward_direction;
                }
                else{
                    current_direction = back_direction;
                }
                pulse++;
            }
        }
    }
}

void testingT_start()
{
    gettimeofday(&StartTime, NULL);  //measure the time
}

double testingT_end()
{
    gettimeofday(&EndTime, NULL);   //measurement ends
    TimeUse = 1000000*(EndTime.tv_sec-StartTime.tv_sec)+EndTime.tv_usec-StartTime.tv_usec;
    TimeUse/=1000;  //the result is in the ms dimension
    return TimeUse;
}

static volatile int file_state = 1;

void intHandler(int i){
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);
    file_state = 0;
}

void *Timer_5ms(void)
{   
    testingT_start();

    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,1);

    int Electromagnet_1_Clutch = 0;
    int Electromagnet_2_Clutch = 1;

    FILE *fp = fopen("./robotic_arm.csv", "w+");
    if (fp == NULL) {
        fprintf(stderr, "fopen() failed.\n");
        printf("Failed\n");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Time,Degree,Velocity,Electromagnet_1_Clutch,Electromagnet_2_Clutch\n");
    
    signal(SIGINT, intHandler);
    while(1){
        get_info();
        
        if(file_state == 1)
            fprintf(fp,"%.2f,%.2f,%.2f,%d,%d\n",testingT_end(),motion,velocity,Electromagnet_1_Clutch,Electromagnet_2_Clutch);
        else
            fclose(fp); 
        if(motion > 45)
            direction_state = forward_direction;
        if(motion <= 0.3 && file_state == 1 && direction_state == forward_direction){
            digitalWrite(electromagnet_1,1);
            digitalWrite(electromagnet_2,0);
            Electromagnet_1_Clutch = 1;
            Electromagnet_2_Clutch = 0;
        }
        delay(5);
    }
}



int main(int argc, const char *argv[])
{
    wiringPiSetup();
    pinMode(encoderB_pin, INPUT);
    
    pinMode(electromagnet_1, OUTPUT);
    pinMode(electromagnet_2, OUTPUT);
    pinMode(electromagnet_3, OUTPUT);
    pinMode(electromagnet_4, OUTPUT);
    
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);
    delay(500);
    
	pthread_t id1,id2;
	int value;

    value = pthread_create(&id1, NULL, (void *)create, NULL);
	if(value){
        printf("thread1 is not created!\n");
        return -1;
	}

    value = pthread_create(&id2, NULL, (void *)Timer_5ms, NULL);
	if(value){
        printf("thread2 is not created!\n");
        return -1;
	}
    printf("All the thread is created..\n");
    
    pthread_join(id1,NULL);
	pthread_join(id2,NULL);
	return 0;
}

