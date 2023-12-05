#ifndef _HMC5883L_H_
#define _HMC5883L_H_
#include <stdint.h>

#define MAG0MAX 603
#define MAG0MIN -578

#define MAG1MAX 542
#define MAG1MIN -701

#define MAG2MAX 547
#define MAG2MIN -556

class HMC5883L {
    public:
        HMC5883L();
        
        static void setmode_continuous();
        static void calibrate();
        static void getdata();
        static void HMC5883L_Write(uint8_t register_address, uint8_t data);
        static uint8_t HMC5883L_Read(uint8_t register_address, uint8_t buffer[], uint8_t length);
    
        static double magX, magY, magZ;
        static uint8_t Data[6];
        static int16_t magPosOff[3];
        static int16_t magNegOff[3];
        static double magGain[3];
        static float magOffset[3];
        
};

#endif