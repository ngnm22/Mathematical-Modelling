# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 09:35:22 2021

@author: jmcha
"""
import numpy as np
import scipy . optimize
import matplotlib . pyplot as plt
import math
G = 6.673e-11
M_E = 5.97e24
R_E = 6370e3
B = 4.63e30
h0 = 1
filename = "data/AthmDensity.csv"
import warnings

warnings.filterwarnings('ignore')

data = np . genfromtxt ( filename , delimiter =',', skip_header=1)
height, density = zip(*data)
height = np.array (height)
h = height

def func_data (h,d,fraction):
    """ Fitting function for exponential data
    : param d : day
    : param A : Amplitude
    : param k : Rate""" 
    #broke down equations to make sure each part worked
    #better layout of equation is outlined in essay
    s = 7.57
    eq1 =((h*1000)**(s+1))
    eq2 = 4*(s+1)
    eq3 = math.sqrt(G*M_E*R_E)
    eq4 = (eq1/(eq2*B*eq3))
    return(eq4*fraction)
def func_log (h,a,l,s) :
    """ Fitting function for exponential data
    32 : param d : day
    33 : param A : Amplitude
    34 : param k : Rate
    35 """
    B = 8.82*10**7
    #if (a >=0) : a =1.946 # Avoid error when A <= 0
    return np.log(((a*np.exp((-h*l))) + B*((h/h0)**(-s))))
#popt_data ,pcov= scipy.optimize.curve_fit (func_log ,height,np.log(density))
popt_data ,_= scipy.optimize.curve_fit (func_log ,height,np.log(density))

a,l,s = popt_data
print("a=", a, "l=",l, "s=",s)
plt.xlabel ("h", fontsize =20)
plt.ylabel ("dens", fontsize =20)
plt.semilogy(height, density, '*', label='data')
plt.semilogy(height, np.exp(func_log(height,*popt_data)), '-r', label='fit')
plt.tight_layout ( rect =[0 , 0 , 1 , 1])
plt.title("curve fit for height against density")
plt.legend()
plt.show() 

#For Q7
#the ratios found in my Q7
v = [27,54,5.4,3850/(np.pi*(3/2)**2)]
labels = ["Ex 4","Ex 5","Ex 6","Ex 7"]
plotting = ['k-','g-','b-','r-']
data = np . genfromtxt ( filename , delimiter =',', skip_header=9)
height, density = zip(*data)
height = np.array (height)
density = np.array (density)
for i in range(len(v)):
    t_list = []
    length = len(height)
    for j in range(length):
        function = func_data(height[j],density[j],v[i])
        conversion = function/(60*60*24*365.25)
        t_list.append(conversion)
    plt.subplots_adjust(left=0.15)
    plt.tight_layout ( rect =[0 , 0 , 1 , 1]) 
    logged = np.log(t_list)
    plt.semilogy((height*1000),t_list, plotting[i],label = labels[i])
plt.title("Logarithmic graph of t(h) against h")
plt.xlabel ("h (m)", fontsize =20)
plt.ylabel ("log(t(h)) (years)", fontsize =20)
plt.legend()
plt.show() 
