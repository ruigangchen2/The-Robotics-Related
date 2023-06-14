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

gcc -o Robotics_Arm_Force_Length Robotics_Arm_Force_Length.c -lwiringPi -pthread -lcrypt -lm -lrt


echo 92 > /sys/class/gpio/export  # Encoder A Phase 
echo in > /sys/class/gpio/gpio92/direction
echo falling > /sys/class/gpio/gpio92/edge
*/


#define electromagnet 3
#define encoderB_pin 15
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

double TimeDuration_Encoder=0;
struct timeval StartTime_Encoder;
struct timeval EndTime_Encoder;
/******************************/

struct pollfd fds[1];

void testingT_durationT_start_Encoder()
{
    gettimeofday(&StartTime_Encoder, NULL);  //measure the time of encoder use
}

double testing_durationT_End_Encoder()
{
    gettimeofday(&EndTime_Encoder, NULL);   //measurement ends
    TimeDuration_Encoder = 1000000*(EndTime_Encoder.tv_sec-StartTime_Encoder.tv_sec)+EndTime_Encoder.tv_usec-StartTime_Encoder.tv_usec;
    TimeDuration_Encoder/=1000;  //the result is in the ms dimension
    return TimeDuration_Encoder;
}

void get_info()  //calculate the information of the encoder
{

    velocity = pulse * 240.0 / (testing_durationT_End_Encoder()); //   n / ((testing_durationT_End_Encoder / 1000) * 1500) * 360

    if(current_direction == forward_direction){
        motion = motion + pulse * 360 / 1500; //calculate the positive motion 
    }
    else{
        motion = motion - pulse * 360 / 1500; //calculate the negative motion 
        velocity = -velocity;
    }
    pulse = 0;    //set pulse to zero
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
                get_info();
                testingT_durationT_start_Encoder();
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
    digitalWrite(electromagnet,0);
    file_state = 0;
}

void *Timer_5ms(void)
{   
    char velocity_state = 0;

    testingT_start();

    digitalWrite(electromagnet,0);

    int Electromagnet_Clutch = 0;
    

    FILE *fp = fopen("./robotic_arm.csv", "w+");
    if (fp == NULL) {
        fprintf(stderr, "fopen() failed.\n");
        printf("Failed\n");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Time,Degree,Velocity,Electromagnet_Clutch\n");
    
    signal(SIGINT, intHandler);
    while(1){
        printf("motion is:%.2f\n",motion);
        // printf("velocity is:%.4f\n",velocity);
        if(file_state == 1)
            fprintf(fp,"%.2f,%.2f,%.2f,%d\n", testingT_end(), motion, velocity, Electromagnet_Clutch);
        else
            fclose(fp); 
        if(file_state == 1){
        digitalWrite(electromagnet,1);
        Electromagnet_Clutch = 1;
        }
        delay(5);
    }
}



int main(int argc, const char *argv[])
{
    wiringPiSetup();
    pinMode(encoderB_pin, INPUT);
    
    pinMode(electromagnet, OUTPUT);
    digitalWrite(electromagnet,0);

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

