#include <stdio.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
//https://zhou-yuxin.github.io/articles/2017/Linux的GPIO子系统之-sys-class-gpio目录/index.html
int main()
{
    int fd=open("/sys/class/gpio/gpio92/value",O_RDONLY);
    if(fd<0)
    {
        perror("open '/sys/class/gpio/gpio92/value' failed!\n");  
        return -1;
    }
    struct pollfd fds[1];
    fds[0].fd=fd;
    fds[0].events=POLLPRI;
    while(1)
    {
        if(poll(fds,1,0)==-1){
            perror("poll failed!\n");
            return -1;
        }
        if(fds[0].revents&POLLPRI)
        {
            if(lseek(fd,0,SEEK_SET)==-1){
                perror("lseek failed!\n");
                return -1;
            }
            char buffer[16];
            int len;
            if((len=read(fd,buffer,sizeof(buffer)))==-1){
                perror("read failed!\n");
                return -1;
            }
            buffer[len]=0;
            printf("%s",buffer);
        }
    }
    return 0;
}