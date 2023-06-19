#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/ioctl.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<sys/select.h>
#include<sys/time.h>
#include<errno.h>
#include<string.h>


#define ADS1115_address                             0x48          //ADS1115地址
#define I2C_SLAVE                                   0x0703       //IIC从器件的地址设置
#define ADS1115_configure                           0x00   //转换寄存器地址
#define ADS1115_register                            0x01   //配置寄存器地址
#define ADS1115_high                                0x82   //高八位 默认通道in0-in1   参考电压4096mv
#define ADS1115_in0_in3                             0x10   //差分in0_in3
#define ADS1115_in1_in3                             0x20   //差分in1_in3
#define ADS1115_in2_in3                             0x30   //差分in2_in3
#define ADS1115_in0                                 0x40   //单端通道0
#define ADS1115_in1                                 0x50   //单端通道1
#define ADS1115_in2                                 0x60   //单端通道2
#define ADS1115_in3                                 0x70   //单端通道3
#define ADS1115_2048                                0x02   //pga 2048
#define ADS1115_1024                                0x04   //pga 1024
#define ADS1115_512                                 0x06   //pga 512
#define ADS1115_256                                 0x08   //pga 256
#define ADS1115_low                                 0xe3   //低八位不动
typedef unsigned char uint8;
int fd = -1;

static uint8 ADS1115_init();
static uint8 ADS1115_write(uint8 ADS1115_GB);
static uint8 ADS1115_read(int fd, uint8 * val);
static uint8 printarray(uint8 Array[], uint8 Num);
short GetData(uint8 passageway, uint8 pga);

static uint8 ADS1115_init()
{
   fd  = open("/dev/i2c-0", O_RDWR);               // open file and enable read and  write

    if (fd < 0)
    {
        perror("Can't open /dev/ADS1115 \n");       // open i2c dev file fail
        exit(1);
    }

    printf("open /dev/i2c-0 success !\n");          // open i2c dev file succes

    if (ioctl(fd, I2C_SLAVE, ADS1115_address) < 0)
    { //set i2c address
        printf("adress failed!\n");
        close(fd);
        return - 1;
    }
    printf("set slave address to 0x%x success!\n", ADS1115_address);
}

static uint8 ADS1115_write(uint8 ADS1115_GB)
{
 

    char buf[3] = {ADS1115_register,ADS1115_GB,ADS1115_low};
    int w_count = 0;
    w_count = write(fd,buf,3);
        //printf("set slave address to 0x%x success!\n", w_count);
    
    return (1);
}

//read byte
static uint8 ADS1115_read(int fd, uint8 * val)
{
    int retries;
    char buf[1] = {ADS1115_configure};
    for (retries = 5; retries; retries--)
    {
        if (write(fd, buf, 1) == 1)
        {
            if (read(fd, val, 1) == 1)
            {
                return 0;
            }

        }

    }

    return - 1;
}

//get data
short GetData(uint8 passageway, uint8 pga)
{
    char H, L;
    uint8 ADS1115_GB = ADS1115_high+passageway+pga;
    ADS1115_write(ADS1115_GB);
    ADS1115_read(fd,  &H);
    usleep(1000);
    ADS1115_read(fd,  &L);
    return (H << 8) +L;
}

int main(int argc, char * argv[])
{
    ADS1115_init();

    while (1)
    {
        // usleep(1000 * 300);
        printf("channe0:%6d\n ", GetData(ADS1115_in0,ADS1115_1024));
        // usleep(1000 * 300);
        // printf("channe1:%6d\n ", GetData(ADS1115_in1,0));
        // usleep(1000 * 300);
        // printf("channe2:%6d\n ", GetData(ADS1115_in2,ADS1115_512));
        // usleep(1000 * 300);
        // printf("channe3:%6d\n ", GetData(ADS1115_in3,ADS1115_1024));
        sleep(1);
    }

    close(fd);
}