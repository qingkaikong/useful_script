#include <stdio.h>
#include <math.h>

double hw1(double r1, double r2)
{
    double s;
    s = sin(r1+r2);
    return s;
}

void hw2(double r1, double r2)
{
    double s;
    s = sin(r1+r2);
    printf ('Hello, World! sin(%g+%g)=%g\n', r1,r2,s);
}

/*special version of hw1 where the result is an argument: */
void hw3(double r1, double r2, double *s)
{
    *s = sin(r1+r2);
}