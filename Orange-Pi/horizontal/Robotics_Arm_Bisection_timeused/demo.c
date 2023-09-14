#include <stdio.h>
#include <stdlib.h>
#include "math.h"
#include <sys/time.h>

#define __USE_GNU
#include <sched.h>
#include <pthread.h>

#include "IIRLowPass.h"

/*

//compile the code
gcc -o demo demo.c IIRLowPass.c -pthread

//run the program in the background
nohup ./demo  & 

//check the frequency of core
sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu1/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu2/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu3/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu5/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu6/cpufreq/cpuinfo_cur_freq
sudo cat /sys/devices/system/cpu/cpu7/cpufreq/cpuinfo_cur_freq

*/

double angle[200] = {-1.07128, -1.06814, -1.06500, -1.06186, -1.05872, -1.05558, -1.05243, -1.04929, -1.04615, -1.04301, -1.03987, -1.03673, -1.03358, -1.03044, -1.02730, -1.02416, -1.02102, -1.01788, -1.01473, -1.01159, -1.00845, -1.00531, -1.00217, -0.99903, -0.99588, -0.99274, -0.98960, -0.98646, -0.98332, -0.98018, -0.97704, -0.97389, -0.97075, -0.96761, -0.96447, -0.96133, -0.95819, -0.95504, -0.95190, -0.94876, -0.94562, -0.94248, -0.93934, -0.93619, -0.93305, -0.92991, -0.92677, -0.92363, -0.92049, -0.91735, -0.91420, -0.91106, -0.90792, -0.90478, -0.90164, -0.89850, -0.89535, -0.89221, -0.88907, -0.88593, -0.88279, -0.87965, -0.87650, -0.87336, -0.87022, -0.86708, -0.86394, -0.86080, -0.85765, -0.85451, -0.85137, -0.84823, -0.84509, -0.84195, -0.83881, -0.83566, -0.83252, -0.82938, -0.82624, -0.82310, -0.81996, -0.81681, -0.81367, -0.81053, -0.80739, -0.80425, -0.80111, -0.79796, -0.79482, -0.79168, -0.78854, -0.78540, -0.78226, -0.77911, -0.77597, -0.77283, -0.76969, -0.76655, -0.76341, -0.76027, -0.75712, -0.75398, -0.75084, -0.74770, -0.74456, -0.74142, -0.73827, -0.73513, -0.73199, -0.72885, -0.72571, -0.72257, -0.71942, -0.71628, -0.71314, -0.71000, -0.70686, -0.70372, -0.70058, -0.69743, -0.69429, -0.69115, -0.68801, -0.68487, -0.68173, -0.67858, -0.67544, -0.67230, -0.66916, -0.66602, -0.66288, -0.65973, -0.65659, -0.65345, -0.65031, -0.64717, -0.64403, -0.64088, -0.63774, -0.63460, -0.63146, -0.62832, -0.62518, -0.62204, -0.61889, -0.61575, -0.61261, -0.60947, -0.60633, -0.60319, -0.60004, -0.59690, -0.59376, -0.59062, -0.58748, -0.58434, -0.58119, -0.57805, -0.57491, -0.57177, -0.56863, -0.56549, -0.56235, -0.55920, -0.55606, -0.55292, -0.54978, -0.54664, -0.54350, -0.54035, -0.53721, -0.53407, -0.53093, -0.52779, -0.52465, -0.52150, -0.51836, -0.51522, -0.51208, -0.50894, -0.50580, -0.50265, -0.49951, -0.49637, -0.49323, -0.49009, -0.48695, -0.48381, -0.48066, -0.47752, -0.47438, -0.47124, -0.46810, -0.46496, -0.46181, -0.45867, -0.45553, -0.45239, -0.44925, -0.44611};
double velocity[200] = {4.05894, 3.77148, 3.79417, 3.77148, 3.79417, 3.81267, 3.61510, 4.08006, 3.81267, 3.83588, 3.81721, 3.80796, 3.83588, 3.80796, 3.83117, 3.79417, 3.80342, 3.77148, 3.79417, 3.79871, 3.79871, 3.83588, 3.81267, 3.82646, 3.80796, 3.79871, 3.81267, 3.80342, 3.83117, 3.82192, 3.84060, 3.60690, 4.04847, 3.79871, 3.77602, 3.78056, 3.77602, 3.79417, 3.78963, 3.78963, 3.79871, 3.78510, 3.77148, 3.78056, 3.78510, 3.79417, 3.78963, 3.78963, 3.76241, 3.76694, 3.74897, 3.75787, 3.75333, 3.75333, 3.76241, 3.74897, 3.74007, 3.72226, 3.74443, 3.74897, 3.75333, 3.76241, 3.77602, 3.76694, 3.56187, 3.97673, 3.74443, 3.73553, 3.74897, 3.75333, 3.75333, 3.73553, 3.74007, 3.54581, 3.95177, 3.72226, 3.73553, 3.73553, 3.75333, 3.74897, 3.74897, 3.54180, 3.96661, 3.74897, 3.74443, 3.73553, 3.73116, 3.72663, 3.72226, 3.49450, 3.97167, 3.51806, 3.94183, 3.71790, 3.72226, 3.72226, 3.71354, 3.71790, 3.73553, 3.73116, 3.73553, 3.73553, 3.74443, 3.72226, 3.72226, 3.72226, 3.51405, 3.92210, 3.70464, 3.70900, 3.71354, 3.70900, 3.71354, 3.71790, 3.52190, 3.95177, 3.73553, 3.72226, 3.72226, 3.72226, 3.71790, 3.70900, 3.71354, 3.51405, 3.92210, 3.70464, 3.69172, 3.69172, 3.69172, 3.70027, 3.70464, 3.71790, 3.71790, 3.71790, 3.71790, 3.71354, 3.70464, 3.70900, 3.49851, 3.70464, 3.91233, 3.70464, 3.69591, 3.69172, 3.68736, 3.68736, 3.70027, 3.70027, 3.70900, 3.68736, 3.72663, 3.70900, 3.70464, 3.69591, 3.51021, 3.90744, 3.68736, 3.68299, 3.67444, 3.67863, 3.68299, 3.68299, 3.68736, 3.68299, 3.68736, 3.68299, 3.67863, 3.68736, 3.68299, 3.68736, 3.70027, 3.69172, 3.68736, 3.67863, 3.67444, 3.68299, 3.67008, 3.67008, 3.47146, 3.88336, 3.67863, 3.67444, 3.66589, 3.67444, 3.66589, 3.68299, 3.48298, 3.88807, 3.67008, 3.66589, 3.67008, 3.66589, 3.66589, 3.66589, 3.47530, 3.87376, 3.65297, 3.64879, 3.65734, 3.67444};
double velocity_filtered[200] = {0.0};

/***** Filter *****/
double a[9] = {1.0, -7.1949243584232745, 22.68506299943664, -40.93508346568443, 46.23642584093399, -33.471920313990374, 15.165671058595017, -3.9317654914649003, 0.44653398238846237};
double b[9] = {9.835591130971311e-10, 7.868472904777049e-09, 2.753965516671967e-08, 5.507931033343934e-08, 6.884913791679918e-08, 5.507931033343934e-08, 2.753965516671967e-08, 7.868472904777049e-09, 9.835591130971311e-10};
/******************************/


/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

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

double fun(double cur_velocity, double t_velocity, double ave_velocity, double rotation_inertia)
{
    double damp = 0.000037;
    return (cur_velocity * cur_velocity - t_velocity * t_velocity) / (2 * damp * ave_velocity / rotation_inertia);
}

void bisection (double *x, double a, double b, int *itr)
{
    *x=(a+b)/2;
    ++(*itr);
    printf("Iteration No.%3d, rotation inertia = %6.10f Kg·m², time used = %f ms\n", *itr, *x, testingT_end());
}




void *create(void)
{
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(7,&mask);
    if (sched_setaffinity(0,sizeof(mask),&mask)<0){
        printf("affinity set fail!");
    }


    testingT_start();

    double initial_inertia_1 = 1.0, initial_inertia_2 = 0.000001, estitated_inertia = 0.0;
    double err_angle = 0.0, cur_velocity = 0.0, t_velocity = 0.0, ave_velocity = 0.0;
    double err = 0.0, err_dest = 0.00001;
    int index = 167;
    int itr = 0;
    int maxmitr = 50;

    int nRet = filtfilt(velocity, velocity_filtered, 200, a, b, 9);
    bisection (&estitated_inertia, initial_inertia_1, initial_inertia_2, &itr);

    do
    {
        err_angle = angle[index + 10] - angle[index];
        cur_velocity = velocity_filtered[index + 1];
        t_velocity = velocity_filtered[index + 10 + 1];
        ave_velocity = (cur_velocity + t_velocity) * 0.5;

        err = err_angle - fun(cur_velocity, t_velocity, ave_velocity, estitated_inertia);

        if (err > 0)
            initial_inertia_2 = estitated_inertia;
        else
            initial_inertia_1 = estitated_inertia;

        bisection (&estitated_inertia, initial_inertia_1, initial_inertia_2, &itr);
        
        if (fabs(err) < err_dest)
        {
            printf("After %d iterations, rotation inertia = %6.10f Kg·m²\n", itr, estitated_inertia);
            
            return 0;
        }
    }
    while (itr < maxmitr);

    printf("The solution does not converge or iterations are not sufficient");
    
    
}



int main(int argc, const char *argv[])
{   

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

