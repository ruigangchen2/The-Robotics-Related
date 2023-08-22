#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "IIRLowPass.h"

/* 
gcc -o test Bisection_Estimate_Numerical_Solution.c IIRLowPass.c
*/

double angle[100] = {-1.38544, -1.38230, -1.37916, -1.37602, -1.37288, -1.36973, -1.36659, -1.36345, -1.36031, -1.35717, -1.35403, -1.35088, -1.34774, -1.34460, -1.34146, -1.33832, -1.33518, -1.33204, -1.32889, -1.32575, -1.32261, -1.31947, -1.31633, -1.31319, -1.31004, -1.30690, -1.30376, -1.30062, -1.29748, -1.29434, -1.29119, -1.28805, -1.28491, -1.28177, -1.27863, -1.27549, -1.27235, -1.26920, -1.26606, -1.26292, -1.25978, -1.25664, -1.25350, -1.25035, -1.24721, -1.24407, -1.24093, -1.23779, -1.23465, -1.23150, -1.22836, -1.22522, -1.22208, -1.21894, -1.21580, -1.21265, -1.20951, -1.20637, -1.20323, -1.20009, -1.19695, -1.19381, -1.19066, -1.18752, -1.18438, -1.18124, -1.17810, -1.17496, -1.17181, -1.16867, -1.16553, -1.16239, -1.15925, -1.15611, -1.15296, -1.14982, -1.14668, -1.14354, -1.14040, -1.13726, -1.13411, -1.13097, -1.12783, -1.12469, -1.12155, -1.11841, -1.11527, -1.11212, -1.10898, -1.10584, -1.10270, -1.09956, -1.09642, -1.09327, -1.09013, -1.08699, -1.08385, -1.08071, -1.07757, -1.07442};
double velocity[100] = {3.73116, 3.55384, 3.81721, 3.99698, 4.11741, 3.78510, 5.10003, 3.90256, 4.52023, 3.54581, 3.85945, 3.80796, 3.63186, 4.43733, 4.16662, 4.26855, 4.58620, 3.98179, 3.90256, 3.71354, 3.67008, 3.59451, 4.06417, 3.96172, 3.87847, 4.17762, 4.08006, 3.95177, 3.99698, 3.61929, 3.59869, 3.88336, 3.88807, 3.98179, 3.78056, 3.91722, 3.80796, 3.96172, 3.95177, 3.87376, 3.93676, 3.78963, 4.02246, 3.85473, 3.88336, 3.88807, 3.74897, 3.80342, 4.15004, 3.95666, 3.93676, 3.79417, 3.87847, 3.79871, 3.87376, 3.85473, 3.64879, 4.23958, 3.88807, 3.97167, 3.83117, 3.83117, 3.87376, 3.83117, 3.94671, 3.82192, 3.87376, 3.88807, 3.87847, 3.85473, 3.82192, 3.83117, 3.86416, 3.68736, 3.87847, 4.06941, 3.84060, 3.83117, 3.85002, 3.85945, 3.80342, 3.85945, 3.63186, 4.05894, 3.80342, 3.76694, 3.78510, 3.80342, 3.86416, 3.83588, 3.65297, 4.08529, 3.82646, 3.84060, 3.78963, 3.82192, 3.80342, 3.83117, 3.85473, 3.61510};
double velocity_filtered[100] = {0.0};
double time[100] = {11.43509, 11.43598, 11.43680, 11.43759, 11.43835, 11.43918, 11.43979, 11.44060, 11.44130, 11.44218, 11.44300, 11.44382, 11.44469, 11.44539, 11.44615, 11.44688, 11.44757, 11.44836, 11.44916, 11.45001, 11.45087, 11.45174, 11.45251, 11.45330, 11.45412, 11.45487, 11.45564, 11.45643, 11.45722, 11.45809, 11.45896, 11.45977, 11.46058, 11.46137, 11.46220, 11.46300, 11.46382, 11.46462, 11.46541, 11.46622, 11.46702, 11.46785, 11.46863, 11.46945, 11.47025, 11.47106, 11.47190, 11.47273, 11.47348, 11.47428, 11.47508, 11.47591, 11.47671, 11.47754, 11.47835, 11.47917, 11.48003, 11.48077, 11.48158, 11.48237, 11.48319, 11.48401, 11.48482, 11.48564, 11.48644, 11.48726, 11.48807, 11.48888, 11.48969, 11.49050, 11.49133, 11.49215, 11.49296, 11.49381, 11.49462, 11.49539, 11.49621, 11.49703, 11.49785, 11.49866, 11.49949, 11.50030, 11.50117, 11.50194, 11.50277, 11.50360, 11.50443, 11.50526, 11.50607, 11.50689, 11.50775, 11.50852, 11.50934, 11.51016, 11.51099, 11.51181, 11.51263, 11.51345, 11.51427, 11.51514};


/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

/***** Estimation *****/
double inertia = 0.001;
double a_inertia = 0.0000000001;
double b_inertia = 1;
double damp = 0.00004;
double h = 0.00089;
double x = 0.0;
double y[2] = {0.0, 0.0};   //声明变量，y0,y1使用数组y[0],y[1]表示
int max_estimation_matrix = 100;
double experiment_angle_matrix[100] = {0.0};
double experiment_velocity_matrix[100] = {0.0};
double estimation_angle_matrix[100] = {0.0};
double estimation_velocity_matrix[100] = {0.0};
double estimation_error = 1;
char estimation_initialize = 0;
/******************************/

/***** Filter *****/
double a[9] = {1.0, -7.1949243584232745, 22.68506299943664, -40.93508346568443, 46.23642584093399, -33.471920313990374, 15.165671058595017, -3.9317654914649003, 0.44653398238846237};
double b[9] = {9.835591130971311e-10, 7.868472904777049e-09, 2.753965516671967e-08, 5.507931033343934e-08, 6.884913791679918e-08, 5.507931033343934e-08, 2.753965516671967e-08, 7.868472904777049e-09, 9.835591130971311e-10};
/******************************/

void rungekutta(double(*function)(double x , double y[] , int j), double x ,  double *y , double h){
    double ywork[2] , k0[2] , k1[2] , k2[2] , k3[2] ;
    int j;
    for(j = 0 ; j < 2 ; ++ j)
        k0[j] = h * (*function)(x , y , j);   //计算k1
    for(j = 0 ; j < 2 ; ++ j)
        ywork[j] = y[j] + 0.5 * k0[j] ;    
         //用数组ywork存储y的变化量
    for(j = 0 ; j < 2 ; ++ j)
        k1[j] = h * (*function)(x + 0.5 * h , ywork , j);//计算k2
    for(j = 0 ; j < 2 ; ++ j)
        ywork[j] = y[j] + 0.5 * k1[j] ;   
         //将y的变化量存储到ywork中
    for(j = 0 ; j < 2 ; ++ j)
        k2[j] = h * (*function)(x + 0.5 * h , ywork , j);//计算k3
    for(j = 0 ; j < 2 ; ++ j)
        ywork[j] = y[j] + k2[j] ;   
        //更新ywork数组，存储y的变化量
    for(j = 0 ; j < 2 ; ++ j)
        k3[j] = h * (*function)(x + h , ywork , j) ;   //计算k4
    for(j = 0 ; j < 2 ; ++ j)
        y[j] = y[j] + (k0[j] + 2 * k1[j] + 2 * k2[j] + k3[j]) / 6;     //计算y0和y1，用j循环先求y0，再求y1
}

double EOM(double x , double y[] , int j){
    if(j == 1)
        return - damp * y[1] / inertia;
    return y[1] ;  
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

int main()
{   
    int nRet = filtfilt(velocity, velocity_filtered, 100, a, b, 9);

    while(max_estimation_matrix != 0){
        experiment_angle_matrix[100 - max_estimation_matrix] = angle[100 - max_estimation_matrix];
        experiment_velocity_matrix[100 - max_estimation_matrix] = velocity_filtered[100 - max_estimation_matrix];
        --max_estimation_matrix;
    }
    if(max_estimation_matrix == 0){
        if(estimation_initialize == 0){
            x = time[0];
            y[0] = experiment_angle_matrix[0];
            y[1] = experiment_velocity_matrix[0];
            estimation_initialize = 1;
        }
        while(fabs(estimation_error) > 0.0005){
            inertia = (a_inertia + b_inertia) / 2;
            x = time[0];
            y[0] = experiment_angle_matrix[0];
            y[1] = experiment_velocity_matrix[0];
            // printf("n = 0: x = %lf, y0 = %lf, y1 = %lf\n" , x , y[0] * 180.0 / M_PI , y[1]) ;
            for(int i = 0; i < 100; ++ i){
                rungekutta(EOM, x , y , h); 
                x = x + h;
                estimation_angle_matrix[i] = y[0];
                estimation_velocity_matrix[i] = y[1];
                // printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , i + 1 , x , y[0] * 180.0 / M_PI , y[1]) ;
            }
            for(int j = 0; j < 100; j++){
                estimation_error += (experiment_angle_matrix[j] - estimation_angle_matrix[j]);
                // printf("The error is: %f \n", fabs(estimation_error));
            }
            if (estimation_error > 0)
                a_inertia = inertia;
            else
                b_inertia = inertia;
            printf("The inertia is: %.10f kg*m^2\n",inertia);
        } 
        
    }

	return 0;
}