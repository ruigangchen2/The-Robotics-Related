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
nohup ./Robotics_Arm_Demo  & 

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
    // velocity = 0.8 * pre_velocity + 0.2 * velocity;
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
    // pre_velocity = velocity;
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

void *create(void)
{
    // cpu_set_t mask;
    // CPU_ZERO(&mask);
    // CPU_SET(3,&mask);
    // if (sched_setaffinity(0,sizeof(mask),&mask)<0){
    //     printf("affinity set fail!");
    // }

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

    char State0 = 0;
    char State1 = 0;
    
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

                printf("\rThe angle is: %.2f degrees, The velocity is: %.2f degrees/s", motion, velocity);   
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
                    if(motion < -65)State0 = 1;
                
                    if(motion > -60 && State0 == 1){
                        digitalWrite(electromagnet_2,0);
                        digitalWrite(electromagnet_1,1);
                        Electromagnet_Clutch_2 = 0;
                        Electromagnet_Clutch_1 = 1;
                    
                        if(motion > 30 && State0 == 1){
                            digitalWrite(electromagnet_4,0);
                              digitalWrite(electromagnet_3,1);
                        
                            Electromagnet_Clutch_4 = 0;
                            Electromagnet_Clutch_3 = 1;

                            if(velocity < 5){
                                digitalWrite(electromagnet_3,0);
                                digitalWrite(electromagnet_4,1);
                                digitalWrite(electromagnet_2,1);
                                digitalWrite(electromagnet_1,1);
                                
                                Electromagnet_Clutch_3 = 0;
                                Electromagnet_Clutch_4 = 1;
                                Electromagnet_Clutch_1 = 1;
                                Electromagnet_Clutch_2 = 0;
                                State0 = 0;
                                State1 = 1;
                            }
                        }
                    }
                    else if(State1 == 0){
                        digitalWrite(electromagnet_1,0);
                        digitalWrite(electromagnet_2,1);
                        Electromagnet_Clutch_1 = 0;
                        Electromagnet_Clutch_2 = 1;
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
    
	pthread_t id1;
	int value;

    value = pthread_create(&id1, NULL, (void *)create, NULL);
    pthread_setname_np(id1, "create");
	if(value){
        printf("thread1 is not created!\n");
        return -1;
	}

    printf("All the thread is created..\n");
    
    pthread_join(id1,NULL);
    
	return 0;
}

