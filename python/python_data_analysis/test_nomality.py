import numpy as np
from scipy.stats import shapiro
from scipy.stats import anderson
from scipy.stats import normaltest

N = 10000
normal_values = np.random.normal(size=N)
zero_values = np.zeros(N)
print "Normal Values Shapiro", shapiro(normal_values)
print "Zeroes Shapiro", shapiro(zero_values)
print
print "Normal Values Anderson", anderson(normal_values)
print "Zeroes Anderson", anderson(zero_values)
print
print "Normal Values normaltest", normaltest(normal_values)
print "Zeroes normaltest", normaltest(zero_values)

'''
normaltest returns a 2-tuple of the chi-squared statistic, and the associated p-value. 
Given the null hypothesis that x came from a normal distribution, the p-value represents 
the probability that a chi-squared statistic that large (or larger) would be seen.

If the p-val is very small, it means it is unlikely that the data came from a normal 
distribution
'''