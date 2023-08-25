#include <stdio.h>
#include <stdlib.h>
#include <math.h>
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
#include <sys/stat.h>

#include "IIRLowPass.h"

/*

//compile the code
gcc -o Robotics_Arm Robotics_Arm.c IIRLowPass.c -lwiringPi -pthread -lcrypt -lm -lrt

//run the program in the background
nohup ./Robotics_Arm_Demo  & 

//check the thread's pid
ps -T -p <pid> 

//check the frequency of core
sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq

//initialize the pin
echo 92 > /sys/class/gpio/export  # Encoder A Phase 
echo in > /sys/class/gpio/gpio92/direction
echo falling > /sys/class/gpio/gpio92/edge
*/

#define encoderB_pin 15
#define electromagnet_1 3
#define electromagnet_2 4
#define electromagnet_3 6
#define electromagnet_4 9

/***** AB encoder variable *****/
float pulse = 0;  //count the pulse of the encoder
float motion = 0; 
float velocity = 0; 
char forward_direction = '+';
char back_direction = '-';
char current_direction = 0; 
char direction_state = 0;
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
float time_matrix[15000] = {0};
float motion_matrix[15000] = {0};
float velocity_matrix[15000] = {0};
int state1_matrix[15000] = {0};
int state2_matrix[15000] = {0};
int state3_matrix[15000] = {0};
int state4_matrix[15000] = {0};
/******************************/

/***** bisection *****/
double initial_inertia_1 = 1.0, initial_inertia_2 = 0.000001, estitated_inertia = 0.0;
double err_angle = 0.0, cur_velocity = 0.0, t_velocity = 0.0, ave_velocity = 0.0;
double err = 0.0, err_dest = 0.0001;
int itr = 0;
int maxmitr = 30;
int max_matrix = 0;
int index = 200;
double angle_bisection[300] = {0.0};
double velocity_bisection[300] = {0.0};
double velocity_filtered[300] = {0.0};
char bisection_state = 0;
/******************************/

/***** Calculated Clutching Angle *****/
double w1 = 3.36;
double w2 = 2.26;
double k1 = 0;
double k2 = 0;
double slope1 = 0.108;
double slope2 = 0.182;
double t1 = 0;
double t2 = 0;
double t3 = 0;
double theta_start = 70 * M_PI / 180;
double theta_goal = 150 * M_PI / 180;
double theta_acc = 10 * M_PI / 180;
double clutching_angle = 0;
/******************************/

/***** Filter *****/
double a[9] = {1.0, -7.1949243584232745, 22.68506299943664, -40.93508346568443, 46.23642584093399, -33.471920313990374, 15.165671058595017, -3.9317654914649003, 0.44653398238846237};
double b[9] = {9.835591130971311e-10, 7.868472904777049e-09, 2.753965516671967e-08, 5.507931033343934e-08, 6.884913791679918e-08, 5.507931033343934e-08, 2.753965516671967e-08, 7.868472904777049e-09, 9.835591130971311e-10};
/******************************/

double calculated_clutching_angle(double J)
{
    double theta_clutch = 0;
    k1 = J * (w1 * w1);
    k2 = J * (w2 * w2);
    t1 = slope1 * M_PI * k1 / 2 / w1;
    t3 = slope2 * M_PI * k2 / 2 / w2;
    t2 = 0.962 * J;

    theta_clutch = (- (t3 + t2 - k2 * theta_goal) / k2) - \
                    sqrt((((0.5 * k1 * (2 * theta_start * theta_acc - (theta_acc * theta_acc)) \
                    - t1 * theta_acc \
                    + t3 * theta_goal \
                    + t2 * theta_acc \
                    - 0.5 * k2 * (theta_goal * theta_goal)) \
                    / (0.5 * k2)) \
                    + (((t3 + t2 - k2 * theta_goal) / k2) * ((t3 + t2 - k2 * theta_goal) / k2))));
    return theta_clutch * 180 / M_PI - 90;
}


double fun(double cur_velocity, double t_velocity, double ave_velocity, double rotation_inertia)
{
    double damp = 0.000037;
    return (cur_velocity * cur_velocity - t_velocity * t_velocity) / (2 * damp * ave_velocity / rotation_inertia);
}

void bisection (double *x, double a, double b, int *itr)
{
    *x=(a+b)/2;
    ++(*itr);
    printf("Iteration No.%3d, rotation inertia = %6.10f Kg·m²\n", *itr, *x);
}


int suit_inertia()
{
   int nRet = filtfilt(velocity_bisection, velocity_filtered, 300, a, b, 9);
    bisection (&estitated_inertia, initial_inertia_1, initial_inertia_2, &itr);
    do
    {
        err_angle = angle_bisection[index + 20] - angle_bisection[index];
        cur_velocity = velocity_filtered[index + 1];
        t_velocity = velocity_filtered[index + 21];
        ave_velocity = (cur_velocity + t_velocity) * 0.5;

        err = err_angle - fun(cur_velocity, t_velocity, ave_velocity, estitated_inertia);

        if (err > 0)
            initial_inertia_2 = estitated_inertia;
        else
            initial_inertia_1 = estitated_inertia;

        bisection (&estitated_inertia, initial_inertia_1, initial_inertia_2, &itr);
        
        if (fabs(err) < err_dest)
        {
            clutching_angle = calculated_clutching_angle(estitated_inertia);
            printf("After %d iterations, rotation inertia = %6.10f Kg·m²\n", itr, estitated_inertia);
            return 0;
        }
    }
    while (itr < maxmitr);
    printf("The solution does not converge or iterations are not sufficient");
}

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
struct pollfd fds[1];
void *create(void)
{
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(7,&mask);
    if (sched_setaffinity(0,sizeof(mask),&mask)<0){
        printf("affinity set fail!");
    }

    int fd = open("/sys/class/gpio/gpio92/value",O_RDONLY);
    if(fd<0){
        perror("open '/sys/class/gpio/gpio92/value' failed!\n");  
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

    bisection (&estitated_inertia, initial_inertia_1, initial_inertia_2, &itr);
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
                
                // printf("\rThe angle is: %.2f degrees, The velocity is: %.2f degrees/s\t", motion, velocity);   
                // fflush(stdout);  
                
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
                    if(matrix_number > 15000){
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

                        if(motion > -55 && motion < 0){
                            if(max_matrix == 300 && bisection_state == 0){
                                suit_inertia();
                                bisection_state = 1;
                            }   
                            else{
                                angle_bisection[max_matrix] = motion;
                                velocity_bisection[max_matrix] = velocity;
                                max_matrix++;
                            }
                        }
                        if(motion > clutching_angle && State0 == 1){
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
                                printf("\rThe angle is: %.2f degrees, The velocity is: %.2f degrees/s\t", motion, velocity);   
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
                        fprintf(fp,"%.2f,%.2f,%.2f,%d,%d,%d,%d,%lf\n",  time_matrix[j - matrix_number],\
                                                                    motion_matrix[j - matrix_number],\
                                                                    velocity_matrix[j - matrix_number],\
                                                                    state1_matrix[j - matrix_number],\
                                                                    state2_matrix[j - matrix_number],\
                                                                    state3_matrix[j - matrix_number],\
                                                                    state4_matrix[j - matrix_number]);                        
                    }
                    printf("\n\nSaved Over!!!\n\n");
                    fclose(fp); 
                }

                //**********************************For user end****************************************

            }
        }
    }
}



int main(int argc, const char *argv[])
{   
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
    // printf("%f",calculated_clutching_angle(0.000289771348));
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

