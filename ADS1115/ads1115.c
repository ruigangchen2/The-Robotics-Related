#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>

static int fd = 0;

//初始化i2c
//i2c_dev设备文件 i2c_addr 设备地址 
//返回 0
int i2c_init(char *i2c_dev, unsigned char i2c_addr)
{
	int res = 0;
	
	fd = open(i2c_dev, O_RDWR);
	if(fd < 0)
	{
		printf("[%s]:[%d] open i2c file error\r\n", __FUNCTION__, __LINE__);
		return -1;
	}
	res = ioctl(fd,I2C_TENBIT,0);				   //7位模式 
	res = ioctl(fd,I2C_SLAVE, (i2c_addr >> 1));    //设置I2C从设备地址
	
	return res;
}

//读i2c
//buf数据 len长度 
//返回 实际读取的长度 
int i2c_readNbyte(unsigned char *buf, int len)
{
	int res = 0;
	
	res = read(fd, buf,len);
	return res;
}

//写i2c
//buf数据 len长度 
//返回 实际写的长度 
int i2c_writeNbyte(unsigned char *buf, int len)
{
	int res = 0;
	
	res = write(fd, buf,len);
	return res;
}

int i2c_readReg(unsigned int reg_addr, unsigned char *buf, int len)
{
	int res = 0;
	unsigned char buff[2];
	
	buff[0] = reg_addr >> 8;
	buff[1] = reg_addr & 0xff;
	write(fd, buff, 2);
	res = read(fd, buf,len);
	
	return res;
}

int i2c_writeReg(unsigned int reg_addr, unsigned char *buf, int len)
{
	int res = 0,i;
	unsigned char *buff = 0;
	
	buff = (unsigned char *)malloc((len+2));
	buff[0] = reg_addr >> 8;
	buff[1] = reg_addr & 0xff;
	for(i = 0; i < len; i++)
		buff[(i+2)] = buf[i];
	res = write(fd, buff, (len+2));
	free(buff);
	
	return res;
}

int i2c_close()
{
	close(fd);
	return 0;
}

int adc_init()
{
    int ret = 0;
    
    i2c_init("/dev/i2c-1", 0x90);

    return ret;
}

int adc_read()
{
    int ret = 0;
    const unsigned char read_cmd[] = {0x01, 0x8b, 0x83};
    const unsigned char read_reg = 0x00;
    unsigned char read_buff[20] = {0};
    i2c_writeNbyte(read_cmd, 3);
    usleep(200);
    i2c_writeNbyte(&read_reg, 3);
	i2c_readNbyte(read_buff, 2);
    ret = read_buff[0] * 256 + read_buff[1];

    return ret;
}
