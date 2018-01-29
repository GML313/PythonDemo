#coding:utf-8
import numpy as np
from numpy.linalg import *

def input():
    str = 'gml'
    tup = ['gml',1,2]
    tup[2] = 'guan'
    return str
print input()
def main():
    a_list = range(10)
    n_numpy_list = np.array(a_list)
    print map(lambda x:x**2,a_list)
    x = np.array(((1,2,3),(3,4,5)))
    y = x[:,2]
    print y
    z = np.arange(1,10).reshape(3,3)
    print z
    temp1 = np.zeros((2,2,2))
    print "dim%d, shape%d" %(temp1.ndim, temp1.ndim)
    print z.transpose()
    print eig(z)
def mattest():
    import matplotlib.pyplot as plt
    x = np.linspace(-np.pi,np.pi,256,endpoint = True)
    c,s = np.cos(x),np.sin(x)
    plt.figure(1)
    plt.plot(x,c)
    plt.plot(x,s)
    plt.show()
def scipytest():
    from scipy.integrate import quad,dblquad
    from scipy.optimize import minimize
    print(quad(lambda x:np.exp(-x),0,np.inf))
def djangotest():
    import django
    print django.get_version()
if __name__ == '__main__':
    djangotest()