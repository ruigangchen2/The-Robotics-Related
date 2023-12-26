#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>

#include <wiringPi.h>
#include <sys/time.h>
#include <signal.h>

#define __USE_GNU
#include <sched.h>
#include <pthread.h>

#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>

/*

//compile the code
gcc -o Robotics_Arm Robotics_Arm.c -lwiringPi -pthread -lcrypt -lm -lrt

//run the program in the background
nohup ./Robotics_Arm  & 

//check the thread's pid
ps -T -p <pid> 

//check the frequency of core
sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq

//initialize the pin
echo 71 > /sys/class/gpio/export  # Encoder A Phase 
echo in > /sys/class/gpio/gpio71/direction
echo falling > /sys/class/gpio/gpio71/edge
*/

#define encoderB_pin 15
#define electromagnet_1 3
#define electromagnet_2 4
#define electromagnet_3 6
#define electromagnet_4 9

/***** AB encoder variable *****/
float pulse = 0;  //count the pulse of the encoder
float motion = 0; 
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; 
char direction_state = 0;
float velocity = 0; 
float pre_velocity = 0; 
char initialize_state = 0;
/******************************/

/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;

double TimeDuration_Encoder=0;
struct timeval StartTime_Encoder;
struct timeval EndTime_Encoder;
/******************************/

/***** data matrix *****/
float time_matrix[30000] = {0};
float motion_matrix[30000] = {0};
float velocity_matrix[30000] = {0};
int state1_matrix[30000] = {0};
int state2_matrix[30000] = {0};
int state3_matrix[30000] = {0};
int state4_matrix[30000] = {0};
/******************************/

/******** experiment ********/
char State0 = 0;
char State1 = 0;
char Reversal_State = 0;
char timer_State = 0;
char lower_clutch_State = 0;
float start_angle = -10;
float clutch_angle = 30;
float re_clutch_angle = -20;
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

    velocity = pulse * 180 / (testing_durationT_End_Encoder()); //   n / ((testing_durationT_End_Encoder / 1000) * 2000) * 360
    if(initialize_state == 0){
        pulse = 0;
        initialize_state = 1;
    }
    if(current_direction == forward_direction){
        motion = motion + pulse * 360 / 2000; //calculate the positive motion 
    }
    else{
        motion = motion - pulse * 360 / 2000; //calculate the negative motion 
        velocity = -velocity;
    }
    pulse = 0;    //set pulse to zero
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
    
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);
    file_state = 0;
    
}

void *external_interrupt_IRQ(void)
{
    delay(100);
    int fd = open("/sys/class/gpio/gpio71/value",O_RDONLY);
    if(fd<0){
        perror("open '/sys/class/gpio/gpio71/value' failed!\n");  
        return (void *)-1;
    }
    fds[0].fd=fd;
    fds[0].events=POLLPRI;


    testingT_start();
    
    digitalWrite(electromagnet_1,0);
    digitalWrite(electromagnet_2,0);
    digitalWrite(electromagnet_3,0);
    digitalWrite(electromagnet_4,0);
    
    
    int Electromagnet_Clutch_1 = 0;
    int Electromagnet_Clutch_2 = 0;
    int Electromagnet_Clutch_3 = 0;
    int Electromagnet_Clutch_4 = 0;

    int matrix_number = 0;
    FILE *fp = fopen("./data.csv", "w+");
    if (fp == NULL){
        fprintf(stderr, "fopen() failed.\n");
        printf("Failed\n");
        exit(EXIT_FAILURE);
    }
    fprintf(fp, "Time,Degree,Velocity,Electromagnet_Clutch_1,Electromagnet_Clutch_2,Electromagnet_Clutch_3,Electromagnet_Clutch_4\n");
    signal(SIGINT, intHandler);



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

                printf("\rThe angle is: %.2f degrees, The velocity is: %.2f degrees/s    ", motion, velocity);   
                fflush(stdout);  
                
                //**********************************For user****************************************
                if(file_state == 1){
                    time_matrix[matrix_number] = testingT_end();
                    motion_matrix[matrix_number] = motion;
                    velocity_matrix[matrix_number] = velocity;
                    state1_matrix[matrix_number] = Electromagnet_Clutch_1;
                    state2_matrix[matrix_number] = Electromagnet_Clutch_2;
                    state3_matrix[matrix_number] = Electromagnet_Clutch_3;
                    state4_matrix[matrix_number] = Electromagnet_Clutch_4;
                    ++matrix_number;
                    if(matrix_number > 30000){
                        printf("\n\nMatrix number error!\n\n");
                        return (void *)-1;
                    }

                #if 1
                if(Reversal_State == 0 && timer_State == 0){
                    if(motion < (start_angle - 5))State0 = 1;

                    if(motion > start_angle && State0 == 1){
                        digitalWrite(electromagnet_1,1);
                        digitalWrite(electromagnet_2,0);
                        digitalWrite(electromagnet_3,0);  
                        digitalWrite(electromagnet_4,1);
                                   
                        Electromagnet_Clutch_1 = 1;
                        Electromagnet_Clutch_2 = 0;
                        Electromagnet_Clutch_3 = 0;
                        Electromagnet_Clutch_4 = 1;
                    
                        if(motion > clutch_angle && State0 == 1){
                            digitalWrite(electromagnet_1,1);
                            digitalWrite(electromagnet_2,0);
                            digitalWrite(electromagnet_3,1);  
                            digitalWrite(electromagnet_4,0);
                                    
                            Electromagnet_Clutch_1 = 1;
                            Electromagnet_Clutch_2 = 0;
                            Electromagnet_Clutch_3 = 1;
                            Electromagnet_Clutch_4 = 0;

                            if(velocity < 5){

                                digitalWrite(electromagnet_1,1);
                                digitalWrite(electromagnet_2,0);
                                digitalWrite(electromagnet_3,1);  
                                digitalWrite(electromagnet_4,1);
                                        
                                Electromagnet_Clutch_1 = 1;
                                Electromagnet_Clutch_2 = 0;
                                Electromagnet_Clutch_3 = 1;
                                Electromagnet_Clutch_4 = 1;

                                State0 = 0;
                                State1 = 1;
                                Reversal_State = 1;
                            }
                        }
                    }
                    else if(State1 == 0){
                        digitalWrite(electromagnet_1,0);
                        digitalWrite(electromagnet_2,1);
                        digitalWrite(electromagnet_3,0);  
                        digitalWrite(electromagnet_4,1);
                        Electromagnet_Clutch_1 = 0;
                        Electromagnet_Clutch_2 = 1;
                        Electromagnet_Clutch_3 = 0;
                        Electromagnet_Clutch_4 = 1;
                    }
                }
                    
                if(Reversal_State == 1 && timer_State == 1 && lower_clutch_State == 0){

                    if(motion <= (clutch_angle)){
                        digitalWrite(electromagnet_1,1);
                        digitalWrite(electromagnet_2,0);
                        digitalWrite(electromagnet_3,0);
                        digitalWrite(electromagnet_4,1);
                        Electromagnet_Clutch_1 = 1;
                        Electromagnet_Clutch_2 = 0;  
                        Electromagnet_Clutch_3 = 0;
                        Electromagnet_Clutch_4 = 1;
                        
                        if(motion < re_clutch_angle){
                            digitalWrite(electromagnet_1,0);
                            digitalWrite(electromagnet_2,1);
                            digitalWrite(electromagnet_3,0);
                            digitalWrite(electromagnet_4,1);
                            Electromagnet_Clutch_1 = 0;
                            Electromagnet_Clutch_2 = 1;  
                            Electromagnet_Clutch_3 = 0;
                            Electromagnet_Clutch_4 = 1;

                            if(velocity > -5){
                                digitalWrite(electromagnet_1,1);
                                digitalWrite(electromagnet_2,1);
                                digitalWrite(electromagnet_3,0);
                                digitalWrite(electromagnet_4,1);
                                Electromagnet_Clutch_1 = 1;
                                Electromagnet_Clutch_2 = 1;  
                                Electromagnet_Clutch_3 = 0;
                                Electromagnet_Clutch_4 = 1;
                                lower_clutch_State = 1;
                            }
                        }
                    }
                    else if(motion > (clutch_angle)){
                        digitalWrite(electromagnet_1,1);
                        digitalWrite(electromagnet_2,0);
                        digitalWrite(electromagnet_3,1);
                        digitalWrite(electromagnet_4,0);
                        Electromagnet_Clutch_1 = 1;
                        Electromagnet_Clutch_2 = 0;  
                        Electromagnet_Clutch_3 = 1;
                        Electromagnet_Clutch_4 = 0;
                        
                    }
                }
                #endif
                }

                if(file_state == 0){
                    int j = matrix_number;
                    while(matrix_number--){
                        fprintf(fp,"%.2f,%.2f,%.2f,%d,%d,%d,%d\n",  time_matrix[j - matrix_number],\
                                                                    motion_matrix[j - matrix_number],\
                                                                    velocity_matrix[j - matrix_number],\
                                                                    state1_matrix[j - matrix_number],\
                                                                    state2_matrix[j - matrix_number],\
                                                                    state3_matrix[j - matrix_number],\
                                                                    state4_matrix[j - matrix_number]);                        
                    }
                    printf("\n\n>>>>>>>>>> Data has been saved Over!!! >>>>>>>>>>\n\n");
                    fclose(fp); 
                }

                //**********************************For user end****************************************

            }
        }
    }
}


void *Timer(void)
{
    while(1){
        if(Reversal_State == 1 && timer_State == 0){
            delay(2000);
            digitalWrite(electromagnet_1,1);
            digitalWrite(electromagnet_2,0);
            digitalWrite(electromagnet_3,1);  
            digitalWrite(electromagnet_4,0);
            timer_State = 1;
        }

        if(lower_clutch_State == 1){
            digitalWrite(electromagnet_1,1);
            digitalWrite(electromagnet_2,1);
            digitalWrite(electromagnet_3,0);
            digitalWrite(electromagnet_4,1);
        }
        
    }
}

int main(int argc, const char *argv[])
{   
    /*
    设置为非阻塞
    */
    int flag1, flag2;
    if(flag1=(fcntl(STDIN_FILENO, F_GETFL, 0)) < 0)
    {
        perror("fcntl");
        return -1;
    }
    flag2 = flag1 | O_NONBLOCK;
    fcntl(STDIN_FILENO, F_SETFL, flag2);

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

    value = pthread_create(&id1, NULL, (void *)external_interrupt_IRQ, NULL);
    pthread_setname_np(id1, "external_interrupt_IRQ");
	if(value){
        printf("thread 'external_interrupt_IRQ' is not created!\n");
        return -1;
	}
    printf("thread 'external_interrupt_IRQ' is created!\n");
    value = pthread_create(&id2, NULL, (void *)Timer, NULL);
    pthread_setname_np(id2, "Timer");
	if(value){
        printf("thread 'Timer' is not created!\n");
        return -1;
	}
    printf("thread 'Timer' is created!\n");
    printf("All the thread is created..\n");
    
    pthread_join(id1,NULL);
	pthread_join(id2,NULL);
	return 0;
}

