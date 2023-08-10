#include <stdio.h>
#include <math.h>

float fun(float t)
{
    return 1.42 * exp(0.05 * t) * sin(-5.47 * t - 1.73) - 0.16;
}
void bisection (float *x, float a, float b, int *itr)
{
    *x=(a+b)/2;
    ++(*itr);
    printf("Iteration no. %3d X = %7.5f\n", *itr, *x);
}

/*
1. maxmitr – maximum number of iterations to be performed
2. x – the value of root at the n th iteration
3. a, b – the limits within which the root lies
4. allerr – allowed error
5. x1 – the value of root at (n+1)th iteration
*/
int main ()
{
    int itr = 0, maxmitr;
    float x, a, b, allerr, x1;
    printf("\nEnter the values of a, b, allowed error and maximum iterations:\n");
    scanf("%f %f %f %d", &a, &b, &allerr, &maxmitr);
    bisection (&x, a, b, &itr);
    do
    {
        if (fun(a)*fun(x) < 0)
            b=x;
        else
            a=x;
        bisection (&x1, a, b, &itr);
        if (fabs(x1-x) < allerr)
        {
            printf("After %d iterations, root = %6.4f\n", itr, x1);
            return 0;
        }
        x=x1;
    }
    while (itr < maxmitr);
    printf("The solution does not converge or iterations are not sufficient");
    return 1;
}