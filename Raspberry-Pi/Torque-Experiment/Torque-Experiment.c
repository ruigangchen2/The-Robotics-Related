#include <stdio.h>  
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
#include <pthread.h>
#include <wiringPi.h>
#include <sys/time.h>
#include <signal.h>
#include <ads1115.h>

/*

gcc -o Raspberry-PI Torque-Experiment.c ads1115.c ads1115.h -lwiringPi -pthread -lcrypt -lm -lrt

*/


#define encoderA_pin 28
#define encoderB_pin 29

#define electromagnet_1 21
#define electromagnet_2 22
#define electromagnet_3 23
#define electromagnet_4 24

/***** AB encoder variable *****/
float pulse = 0;  //count the pulse of the encoder
float motion = 0; 
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; 
char direction_state = 0;
float velocity = 0; 
/******************************/

/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;

double TimeDuration_Encoder=0;
struct timeval StartTime_Encoder;
struct timeval EndTime_Encoder;
/******************************/

/***** ADS1115 *****/
int16_t adc_value;
float Weight, Gain;
float Gain = 1.033499;
/******************************/

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

    velocity = pulse * 180.0 / (testing_durationT_End_Encoder()); //   n / ((testing_durationT_End_Encoder / 1000) * 2000) * 360

    if(current_direction == forward_direction){
        motion = motion + pulse * 360 / 2000; //calculate the positive motion 
    }
    else{
        motion = motion - pulse * 360 / 2000; //calculate the negative motion 
        velocity = -velocity;
    }
    pulse = 0;    //set pulse to zero
}

void IRQ_interrupt(void){
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

void testingT_start()
{
    gettimeofday(&StartTime, NULL);  //measure the time
}

double testingT_end()
{
    gettimeofday(&EndTime, NULL);   //measurement ends
    TimeUse = 1000000*(EndTime.tv_sec-StartTime.tv_sec)+EndTime.tv_usec-StartTime.tv_usec;
    TimeUse /= 1000;  //the result is in the ms dimension
    return TimeUse;
}

static volatile int file_state = 1;

void intHandler(int i){
    file_state = 0;
    delay(5);
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);
    
    
}

void *Timer_5ms(void)
{
    testingT_start();

    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);

    int Electromagnet_Clutch_1 = 0;
    int Electromagnet_Clutch_2 = 0;
    int Electromagnet_Clutch_3 = 0;
    int Electromagnet_Clutch_4 = 0;

    FILE *fp = fopen("./robotic_arm.csv", "w+");
    if (fp == NULL){
        fprintf(stderr, "fopen() failed.\n");
        printf("Failed\n");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Time,Degree,Velocity,Force,Electromagnet_Clutch_1,Electromagnet_Clutch_2,Electromagnet_Clutch_3,Electromagnet_Clutch_4\n");
    
    signal(SIGINT, intHandler);

    while(1){
        

		adc_value = (int16_t) analogRead(100);
		Weight = adc_value * (4.096 / 32768) / 3.3 * 1000 * Gain; // plase find the .h file to change this number

        printf("\rThe angle is: %.2f degrees, The velocity is: %.2f degrees/s, The Weight is: %.2f g", motion, velocity, Weight);   
        fflush(stdout);   

        if(file_state == 1){
            fprintf(fp,"%.2f,%.2f,%.2f,%.2f,%d,%d,%d,%d\n", testingT_end(), motion, velocity, Weight * 0.001 * 9.8, Electromagnet_Clutch_1, Electromagnet_Clutch_2, Electromagnet_Clutch_3, Electromagnet_Clutch_4);
            digitalWrite(electromagnet_2,1);
            Electromagnet_Clutch_2 = 1;
        }
        else
            fclose(fp); 
        delay(5);
    }
}

int main (void)
{
	ads1115Setup(100,0x48);

    wiringPiSetup();
    pinMode(encoderA_pin, INPUT);
    pinMode(encoderB_pin, INPUT);

    pullUpDnControl (encoderA_pin, PUD_UP); 
    delay(100);
    wiringPiISR(encoderA_pin,INT_EDGE_FALLING,&IRQ_interrupt);

    pinMode(electromagnet_1, OUTPUT);
    pinMode(electromagnet_2, OUTPUT);
    pinMode(electromagnet_3, OUTPUT);
    pinMode(electromagnet_4, OUTPUT);
    
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);


    pthread_t id1;
	int value;

    value = pthread_create(&id1, NULL, (void *)Timer_5ms, NULL);
	if(value){
        printf("thread1 is not created!\n");
        return -1;
	}
    printf("All the thread is created..\n");
    
    pthread_join(id1,NULL);

	return 0;
}
