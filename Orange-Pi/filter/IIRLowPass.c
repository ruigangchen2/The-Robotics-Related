#include "stdio.h"
#include <math.h>
#include <memory.h>
#include <stdlib.h>

#define EPS 0.000001

double velocity[] = {1.05819, 1.19049, 1.32453, 1.36764, 1.48754, 1.62944, 1.63118, 1.75214, 1.86785, 
            1.88565, 1.95494, 2.01516, 2.02039, 2.22809, 2.22180, 2.27486, 2.32705, 2.37644, 2.35497, 2.57715, 
            2.53143, 2.57715, 2.52741, 2.68973, 2.86112, 2.77525, 2.81749, 2.86112, 2.78502, 2.94437, 3.14159, 
            3.03251, 3.05607, 3.10128, 3.13845, 3.04420, 3.22537, 3.42591, 3.31037, 3.33498, 3.37808, 3.42224, 
            3.45610, 3.32084, 3.73116, 3.55785, 3.59451, 3.62767, 3.66153, 3.70027, 3.73116, 3.54581, 4.01234, 
            3.82192, 3.80342, 3.73116, 3.55384, 3.81721, 3.99698, 4.11741, 3.78510, 5.10003, 3.90256, 4.52023, 
            3.54581, 3.85945, 3.80796, 3.63186, 4.43733, 4.16662, 4.26855, 4.58620, 3.98179, 3.90256, 3.71354, 
            3.67008, 3.59451, 4.06417, 3.96172, 3.87847, 4.17762, 4.08006, 3.95177, 3.99698, 3.61929, 3.59869, 
            3.88336, 3.88807, 3.98179, 3.78056, 3.91722, 3.80796, 3.96172, 3.95177, 3.87376, 3.93676, 3.78963, 
            4.02246, 3.85473, 3.88336};

double velocity_filtered[100] = {0.0};

//filter函数
void filter(const double* x, double* y, int xlen, double* a, double* b, int nfilt, double* zi)//nfilt为系数数组长度
{
    double tmp;
    int i,j;
    //normalization
    if((*a-1.0>EPS)||(*a-1.0<-EPS)){
        tmp=*a;
        for(i=0;i<nfilt;i++){
            b[i]/=tmp;
            a[i]/=tmp;
        }
    }
    memset(y,0,xlen*sizeof(double));//将y清零，以双浮点为单位
    a[0]=0.0;
    for(i=0;i<xlen;i++){
        for(j=0;i>=j&&j<nfilt;j++){
            y[i] += (b[j]*x[i-j]-a[j]*y[i-j]);
        }
        if(zi&&i<nfilt-1) y[i] += zi[i];
    }
    a[0]=1.0;
}

//矩阵乘法
void trmul(double *a,double *b,double *c,int m,int n,int k)//矩阵乘法  m为a的行数，n为a的列数数，k为b的行数，第一个矩阵列数必须要和第二个矩阵的行数相同
{ 
    int i,j,l,u;
    for (i=0; i<=m-1; i++)
    for (j=0; j<=k-1; j++){ 
        u=i*k+j; c[u]=0.0;
        for (l=0; l<=n-1; l++)
            c[u]=c[u]+a[i*n+l]*b[l*k+j];
    }
    return;
}


//求逆矩阵，当返回值为0时成功，a变为逆矩阵
int rinv(double *a,int n)//逆矩阵
{
    int *is,*js,i,j,k,l,u,v;
    double d,p;
    is=(int *)malloc(n*sizeof(int));
    js=(int *)malloc(n*sizeof(int));
    for (k=0; k<=n-1; k++){ 
        d=0.0;
        for (i=k; i<=n-1; i++)
        for (j=k; j<=n-1; j++){ 
            l=i*n+j; p=fabs(a[l]);
            if (p>d) { d=p; is[k]=i; js[k]=j;}
        }
        if (d+1.0==1.0){ 
            free(is); free(js); printf("err**not invn");
            return(0);
        }
        if (is[k]!=k)
            for (j=0; j<=n-1; j++){ 
                u=k*n+j; v=is[k]*n+j;
                p=a[u]; a[u]=a[v]; a[v]=p;
            }
        if (js[k]!=k)
            for (i=0; i<=n-1; i++){ 
                u=i*n+k; v=i*n+js[k];
                p=a[u]; a[u]=a[v]; a[v]=p;
            }
        l=k*n+k;
        a[l]=1.0/a[l];
        for (j=0; j<=n-1; j++)
            if (j!=k){ 
                u=k*n+j; a[u]=a[u]*a[l];
            }
        for (i=0; i<=n-1; i++)
            if (i!=k)
                for (j=0; j<=n-1; j++)
                    if (j!=k){ 
                        u=i*n+j;
                        a[u]=a[u]-a[i*n+k]*a[k*n+j];
                    }
        for (i=0; i<=n-1; i++)
            if (i!=k){ 
                u=i*n+k; a[u]=-a[u]*a[l];
            }
    }
    for (k=n-1; k>=0; k--){ 
        if (js[k]!=k)
            for(j=0; j<=n-1; j++){ 
                u=k*n+j; v=js[k]*n+j;
                p=a[u]; a[u]=a[v]; a[v]=p;
            }
        if (is[k]!=k)
            for(i=0; i<=n-1; i++){ 
                u=i*n+k; v=i*n+is[k];
                p=a[u]; a[u]=a[v]; a[v]=p;
            }
    }
    free(is);
    free(js);
    return(0);
}

//filtfilt函数
int filtfilt(double* x, double* y, int xlen, double* a, double* b, int nfilt)
{
    int nfact;
    int tlen;    //length of tx
    int i;
    double *tx,*tx1,*p,*t,*end;
    double *sp,*tvec,*zi;
    double tmp,tmp1;

    nfact=nfilt-1;    //3*nfact: length of edge transients
    if(xlen<=3*nfact || nfilt<2) return -1;    
    //too short input x or a,b
    //Extrapolate beginning and end of data sequence using a "reflection
    //method". Slopes of original and extrapolated sequences match at
    //the end points.
    //This reduces end effects.
    tlen=6*nfact+xlen;
    tx=(double *)malloc(tlen*sizeof(double));
    tx1=(double *)malloc(tlen*sizeof(double));


    sp=(double *)malloc( sizeof(double) * nfact * nfact );
    tvec=(double *)malloc( sizeof(double) * nfact );
    zi=(double *)malloc( sizeof(double) * nfact );

    if( !tx || !tx1 || !sp || !tvec || !zi ){
        free(tx);
        free(tx1);
        free(sp);
        free(tvec);
        free(zi);
        return 1;
    }
    
    tmp=x[0];
    for(p=x+3*nfact,t=tx;p>x;--p,++t) 
        *t=2.0*tmp-*p;
    for(end=x+xlen;p<end;++p,++t) 
        *t=*p;
    tmp=x[xlen-1];
    for(end=tx+tlen,p-=2;t<end;--p,++t) 
        *t=2.0*tmp-*p;
    //now tx is ok.

    end = sp + nfact*nfact;
    p=sp;
    while(p<end) *p++ = 0.0L; //clear sp
    sp[0]=1.0+a[1];
    for(i=1;i<nfact;i++){
        sp[i*nfact]=a[i+1];
        sp[i*nfact+i]=1.0L;
        sp[(i-1)*nfact+i]=-1.0L;
    }
    for(i=0;i<nfact;i++){
        tvec[i]=b[i+1]-a[i+1]*b[0];
    }
    if(rinv(sp,nfact)){
        free(zi);
        zi=NULL;
    }
    else{
        trmul(sp,tvec,zi,nfact,nfact,1);
    }//zi is ok
    free(sp);free(tvec);
    //filtering tx, save it in tx1
    tmp1=tx[0];
    if(zi)
        for( p=zi,end=zi+nfact; p<end;) *(p++) *= tmp1;
    filter(tx,tx1,tlen,a,b,nfilt,zi);
    //reverse tx1
    for( p=tx1,end=tx1+tlen-1; p<end; p++,end--){
        tmp = *p;
        *p = *end;
        *end = tmp;
    }
    //filter again
    tmp1 = (*tx1)/tmp1;
    if(zi)
        for( p=zi,end=zi+nfact; p<end;) *(p++) *= tmp1;
    filter(tx1,tx,tlen,a,b,nfilt,zi);//
    //reverse to y
    end = y+xlen;
    p = tx+3*nfact+xlen-1;
    while(y<end){
        *y++ = *p--;
    }
    free(zi);
    free(tx);
    free(tx1);
    return 0;
}

int main()
{

double a[9] = {1.0, -7.1949243584232745, 22.68506299943664, -40.93508346568443, 46.23642584093399, -33.471920313990374, 15.165671058595017, -3.9317654914649003, 0.44653398238846237};
double b[9] = {9.835591130971311e-10, 7.868472904777049e-09, 2.753965516671967e-08, 5.507931033343934e-08, 6.884913791679918e-08, 5.507931033343934e-08, 2.753965516671967e-08, 7.868472904777049e-09, 9.835591130971311e-10};

int nRet = filtfilt(velocity, velocity_filtered, 100, a, b, 9);

for(int i=0;i<100;i++)
{
    printf("velocity[%d] = %.5f, velocit_filtered[%d] = %.5f\n",i, velocity[i], i, velocity_filtered[i]);
}
return 0;
}