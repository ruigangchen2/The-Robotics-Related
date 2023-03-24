#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void *create(void *arg)
{
	int *num;
	num = (int *)arg;
	printf("Create parameter is %d\n",*num);
	return (void *)0;
}
 
int main(int argc, const char *argv[])
{
	pthread_t id1;
	int error;
 
	int test = 4;
	int *attr = &test;
 
	error = pthread_create(&id1,NULL,create,(void *)attr);
 
	if(error)
	{
		printf("Pthread_create is not created!\n");
		return -1;
	}
	sleep(1);
 
	printf("Pthread_create is created..\n");
	return 0;
}
