#include <wiringPi.h>
#include <ads1115.h>
#include <stdio.h>
#include <stdint.h>

int main() 
{
	static char state = 0;

    if (state == 0)
    {
        adc_init();
        state = 1;
    }
	while(1){
    printf("%d\n",adc_read());
	}

	return 0;
}

