#ifndef _IIRLOWPASS_H_
#define _IIRLOWPASS_H_

/*template

int nRet = filtfilt(x, filtered_x, 100, a, b, 9);
for(int i=0;i<100;i++){
    printf("x[%d] = %.5f, filtered_x[%d] = %.5f\n",i, x[i], i, filtered_x[i]);
}

*/
void filter(const double* x, double* y, int xlen, double* a, double* b, int nfilt, double* zi);
void trmul(double *a,double *b,double *c,int m,int n,int k);
int rinv(double *a,int n);
int filtfilt(double* x, double* y, int xlen, double* a, double* b, int nfilt);
#endif