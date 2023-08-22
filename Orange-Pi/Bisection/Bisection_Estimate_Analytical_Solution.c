#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "IIRLowPass.h"

/* 
gcc -o test Bisection_Estimate_Analytical_Solution.c IIRLowPass.c
*/

double angle[200] = {-1.07128, -1.06814, -1.06500, -1.06186, -1.05872, -1.05558, -1.05243, -1.04929, -1.04615, -1.04301, -1.03987, -1.03673, -1.03358, -1.03044, -1.02730, -1.02416, -1.02102, -1.01788, -1.01473, -1.01159, -1.00845, -1.00531, -1.00217, -0.99903, -0.99588, -0.99274, -0.98960, -0.98646, -0.98332, -0.98018, -0.97704, -0.97389, -0.97075, -0.96761, -0.96447, -0.96133, -0.95819, -0.95504, -0.95190, -0.94876, -0.94562, -0.94248, -0.93934, -0.93619, -0.93305, -0.92991, -0.92677, -0.92363, -0.92049, -0.91735, -0.91420, -0.91106, -0.90792, -0.90478, -0.90164, -0.89850, -0.89535, -0.89221, -0.88907, -0.88593, -0.88279, -0.87965, -0.87650, -0.87336, -0.87022, -0.86708, -0.86394, -0.86080, -0.85765, -0.85451, -0.85137, -0.84823, -0.84509, -0.84195, -0.83881, -0.83566, -0.83252, -0.82938, -0.82624, -0.82310, -0.81996, -0.81681, -0.81367, -0.81053, -0.80739, -0.80425, -0.80111, -0.79796, -0.79482, -0.79168, -0.78854, -0.78540, -0.78226, -0.77911, -0.77597, -0.77283, -0.76969, -0.76655, -0.76341, -0.76027, -0.75712, -0.75398, -0.75084, -0.74770, -0.74456, -0.74142, -0.73827, -0.73513, -0.73199, -0.72885, -0.72571, -0.72257, -0.71942, -0.71628, -0.71314, -0.71000, -0.70686, -0.70372, -0.70058, -0.69743, -0.69429, -0.69115, -0.68801, -0.68487, -0.68173, -0.67858, -0.67544, -0.67230, -0.66916, -0.66602, -0.66288, -0.65973, -0.65659, -0.65345, -0.65031, -0.64717, -0.64403, -0.64088, -0.63774, -0.63460, -0.63146, -0.62832, -0.62518, -0.62204, -0.61889, -0.61575, -0.61261, -0.60947, -0.60633, -0.60319, -0.60004, -0.59690, -0.59376, -0.59062, -0.58748, -0.58434, -0.58119, -0.57805, -0.57491, -0.57177, -0.56863, -0.56549, -0.56235, -0.55920, -0.55606, -0.55292, -0.54978, -0.54664, -0.54350, -0.54035, -0.53721, -0.53407, -0.53093, -0.52779, -0.52465, -0.52150, -0.51836, -0.51522, -0.51208, -0.50894, -0.50580, -0.50265, -0.49951, -0.49637, -0.49323, -0.49009, -0.48695, -0.48381, -0.48066, -0.47752, -0.47438, -0.47124, -0.46810, -0.46496, -0.46181, -0.45867, -0.45553, -0.45239, -0.44925, -0.44611};
double velocity[200] = {4.05894, 3.77148, 3.79417, 3.77148, 3.79417, 3.81267, 3.61510, 4.08006, 3.81267, 3.83588, 3.81721, 3.80796, 3.83588, 3.80796, 3.83117, 3.79417, 3.80342, 3.77148, 3.79417, 3.79871, 3.79871, 3.83588, 3.81267, 3.82646, 3.80796, 3.79871, 3.81267, 3.80342, 3.83117, 3.82192, 3.84060, 3.60690, 4.04847, 3.79871, 3.77602, 3.78056, 3.77602, 3.79417, 3.78963, 3.78963, 3.79871, 3.78510, 3.77148, 3.78056, 3.78510, 3.79417, 3.78963, 3.78963, 3.76241, 3.76694, 3.74897, 3.75787, 3.75333, 3.75333, 3.76241, 3.74897, 3.74007, 3.72226, 3.74443, 3.74897, 3.75333, 3.76241, 3.77602, 3.76694, 3.56187, 3.97673, 3.74443, 3.73553, 3.74897, 3.75333, 3.75333, 3.73553, 3.74007, 3.54581, 3.95177, 3.72226, 3.73553, 3.73553, 3.75333, 3.74897, 3.74897, 3.54180, 3.96661, 3.74897, 3.74443, 3.73553, 3.73116, 3.72663, 3.72226, 3.49450, 3.97167, 3.51806, 3.94183, 3.71790, 3.72226, 3.72226, 3.71354, 3.71790, 3.73553, 3.73116, 3.73553, 3.73553, 3.74443, 3.72226, 3.72226, 3.72226, 3.51405, 3.92210, 3.70464, 3.70900, 3.71354, 3.70900, 3.71354, 3.71790, 3.52190, 3.95177, 3.73553, 3.72226, 3.72226, 3.72226, 3.71790, 3.70900, 3.71354, 3.51405, 3.92210, 3.70464, 3.69172, 3.69172, 3.69172, 3.70027, 3.70464, 3.71790, 3.71790, 3.71790, 3.71790, 3.71354, 3.70464, 3.70900, 3.49851, 3.70464, 3.91233, 3.70464, 3.69591, 3.69172, 3.68736, 3.68736, 3.70027, 3.70027, 3.70900, 3.68736, 3.72663, 3.70900, 3.70464, 3.69591, 3.51021, 3.90744, 3.68736, 3.68299, 3.67444, 3.67863, 3.68299, 3.68299, 3.68736, 3.68299, 3.68736, 3.68299, 3.67863, 3.68736, 3.68299, 3.68736, 3.70027, 3.69172, 3.68736, 3.67863, 3.67444, 3.68299, 3.67008, 3.67008, 3.47146, 3.88336, 3.67863, 3.67444, 3.66589, 3.67444, 3.66589, 3.68299, 3.48298, 3.88807, 3.67008, 3.66589, 3.67008, 3.66589, 3.66589, 3.66589, 3.47530, 3.87376, 3.65297, 3.64879, 3.65734, 3.67444};
double velocity_filtered[200] = {0.0};
double time[200] = {11.51591, 11.51675, 11.51757, 11.51841, 11.51924, 11.52006, 11.52093, 11.52170, 11.52252, 11.52334, 11.52417, 11.52499, 11.52581, 11.52663, 11.52745, 11.52828, 11.52911, 11.52994, 11.53077, 11.53160, 11.53242, 11.53324, 11.53407, 11.53489, 11.53571, 11.53654, 11.53736, 11.53819, 11.53901, 11.53983, 11.54065, 11.54152, 11.54229, 11.54312, 11.54395, 11.54479, 11.54562, 11.54645, 11.54728, 11.54810, 11.54893, 11.54976, 11.55059, 11.55142, 11.55225, 11.55308, 11.55391, 11.55474, 11.55558, 11.55641, 11.55725, 11.55808, 11.55892, 11.55976, 11.56059, 11.56143, 11.56227, 11.56312, 11.56395, 11.56479, 11.56563, 11.56646, 11.56730, 11.56813, 11.56901, 11.56980, 11.57064, 11.57148, 11.57232, 11.57316, 11.57399, 11.57483, 11.57567, 11.57656, 11.57736, 11.57820, 11.57904, 11.57988, 11.58072, 11.58156, 11.58240, 11.58328, 11.58408, 11.58491, 11.58575, 11.58659, 11.58743, 11.58828, 11.58912, 11.59002, 11.59082, 11.59171, 11.59250, 11.59335, 11.59419, 11.59504, 11.59588, 11.59673, 11.59757, 11.59841, 11.59925, 11.60009, 11.60093, 11.60178, 11.60262, 11.60346, 11.60436, 11.60516, 11.60601, 11.60686, 11.60770, 11.60855, 11.60939, 11.61024, 11.61113, 11.61193, 11.61277, 11.61361, 11.61446, 11.61530, 11.61614, 11.61699, 11.61784, 11.61873, 11.61953, 11.62038, 11.62123, 11.62208, 11.62293, 11.62378, 11.62463, 11.62548, 11.62632, 11.62717, 11.62801, 11.62886, 11.62971, 11.63055, 11.63145, 11.63230, 11.63310, 11.63395, 11.63480, 11.63565, 11.63650, 11.63736, 11.63821, 11.63905, 11.63990, 11.64075, 11.64160, 11.64244, 11.64329, 11.64414, 11.64504, 11.64584, 11.64669, 11.64754, 11.64840, 11.64925, 11.65011, 11.65096, 11.65181, 11.65267, 11.65352, 11.65437, 11.65522, 11.65608, 11.65693, 11.65778, 11.65863, 11.65948, 11.66033, 11.66119, 11.66204, 11.66289, 11.66375, 11.66461, 11.66551, 11.66632, 11.66718, 11.66803, 11.66889, 11.66974, 11.67060, 11.67145, 11.67236, 11.67316, 11.67402, 11.67488, 11.67573, 11.67659, 11.67745, 11.67830, 11.67921, 11.68002, 11.68088, 11.68174, 11.68260, 11.68345};


/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

/***** Estimation *****/
double inertia = 0;
double inertia_average = 0;
double damp = 0.00003780;
int max_estimation_matrix = 200;
/******************************/

/***** Filter *****/
double a[9] = {1.0, -7.1949243584232745, 22.68506299943664, -40.93508346568443, 46.23642584093399, -33.471920313990374, 15.165671058595017, -3.9317654914649003, 0.44653398238846237};
double b[9] = {9.835591130971311e-10, 7.868472904777049e-09, 2.753965516671967e-08, 5.507931033343934e-08, 6.884913791679918e-08, 5.507931033343934e-08, 2.753965516671967e-08, 7.868472904777049e-09, 9.835591130971311e-10};
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

double equation(double velocity_t, double velocity, double angle)
{
    return 2 * angle * damp * ((velocity_t + velocity) / 2) / (velocity_t * velocity_t - velocity * velocity);
}

int main()
{   
    int nRet = filtfilt(velocity, velocity_filtered, 200, a, b, 9);
    
    for(int i = 0; i < max_estimation_matrix - 19; i++){
        inertia = equation(velocity_filtered[i+1], velocity_filtered[i+1+20], (angle[i+20]-angle[i]));
        inertia_average += inertia;
        printf("n = %d, inertia = %f\n",i,inertia);
    }

    // inertia = equation(velocity_filtered[70], velocity_filtered[90], (angle[90]-angle[70]));
    // printf("inertia = %f\n",inertia);
	return 0;
}