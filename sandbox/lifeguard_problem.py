from math import sqrt
from scipy.optimize import fmin

w1 = 1
w2 = 2
def time(d):
    return w1*sqrt(1/4+d**2)+w2*sqrt(1/4+(1-d)**2)

d_min = fmin(time, 1/2)
cost = time(d_min)
