#include <stdio.h>
#include <wiringPi.h>


void blank(void)
{
    printf("hello");
}

int main (void)
{
    wiringPiSetup();
    pinMode(13, INPUT);
    pullUpDnControl (13, PUD_UP); // 这个很重要，把中断引脚设置成上拉输入，
    delay(100);
    wiringPiISR(13,INT_EDGE_BOTH,&blank);
    while(1);
	return 0;
}
