#include <wiringPi.h>
#include <ads1115.h>
#include <stdio.h>
#include <stdint.h>

/*
gcc ads1115.c ads1115.h ads1115_read.c -lwiringPi -o ads
*/


int main(int argc, char *argv[]) 
{
  
	int16_t value;
  
	float Weight, Gain;
	
	Gain = 1.033499;

	ads1115Setup(100,0x48);

	for (;;) 
	{
    
		value = (int16_t) analogRead(100);
    
		Weight = value * (4.096 / 32768) / 3.3 * 1000 * Gain; // plase find the .h file to change this number
		
		printf("ADS1115 Reading: %d\n\r",value);
    
		printf("The Weight is: %.2f g\n\r",Weight);

		delay(500);
  
	} 
	return 0;
}

