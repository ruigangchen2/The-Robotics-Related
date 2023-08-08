#include <stdio.h>
#include <math.h>
#include <sys/time.h>

/***** Testing time *****/
double TimeUse = 0;
struct timeval StartTime;
struct timeval EndTime;
/******************************/

double inertia = 0.000141407104;
double stiffness1 = 0.0039422038081536;
double stiffness2 = 0.00420014450656;
double angle0 = -1.5582299561805375;
double torque_friction1 = 0.00012666271216345623;
double torque_friction2 = 0.00048422543581007056;



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

double EOM1(double x , double y[] , int j){
    if(j == 1)
        return - (stiffness1 * (y[0] + angle0 * M_PI / 180) - torque_friction1) / inertia;
    return y[1] ;   
}

double EOM2(double x , double y[] , int j){
    if(j == 1)
        return - torque_friction1 / inertia;
    return y[1] ;  
}

double EOM3(double x , double y[] , int j){
    if(j == 1)
        return - (stiffness2 * y[0] - torque_friction2) / inertia;
    return y[1] ;  
}

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

int main() {
    testingT_start();
    double h = 0.001;
    double x1 = 11.36725, x2 = 11.43509, x3 = 11.90949;
    double y1[2], y2[2], y3[2]; //声明变量，y0,y1使用数组y[0],y[1]表示
    y1[0] = -1.5582299561805375, y1[1] = 1.0661065888878667;   //设置运算初始值
    y2[0] = -1.3823007675795091, y2[1] = 3.921637138389167;
    y3[0] = 0.37070793312359557, y3[1] = 3.4755645297730133; 
    
    // printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , 0 , x1 , y1[0] * 180.0 / M_PI , y1[1]) ;
    // for(int i = 0; i < 67; ++ i){
    //     rungekutta(EOM1, x1 , y1 , h); 
    //     x1 = x1 + h;
    //     printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , i + 1 , x1 , y1[0] * 180.0 / M_PI , y1[1]) ;
    // }

    // printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , 0 , x2 , y2[0] * 180.0 / M_PI , y2[1]) ;
    // for(int i = 0; i < 474; ++ i){
    //     rungekutta(EOM2, x2 , y2 , h); 
    //     x2 = x2 + h;
    //     printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , i + 1 , x2 , y2[0] * 180.0 / M_PI , y2[1]) ;
    // }

    // printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , 0 , x3 , y3[0] * 180.0 / M_PI , y3[1]);
    for(int i = 0; i < 196; ++ i){
        rungekutta(EOM3, x3 , y3 , h); 
        x3 = x3 + h;
        // printf("n = %d: x = %lf, y0 = %lf, y1 = %lf\n" , i + 1 , x3 , y3[0] * 180.0 / M_PI , y3[1]) ;
    }
    printf("The time used is: %.3lf ms\n",testingT_end());

    return 0;
}
