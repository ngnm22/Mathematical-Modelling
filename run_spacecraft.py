import gravity as gr
import math
import numpy as np
import matplotlib.pyplot as plt
from spacecraft import *

dt = 0.1
gdt = 1
#s = Spacecraft([0,0,0,0],dt,0,4e5,4000.) # initial condition set later
tmax= 4000
Fr_list = [50,25,10]
Ftheta_list = [100.,50.,20.]
t_thrust_list = [100,200,500]
plotting = ['b-','g-','r-']
for i in range(len(Fr_list)):
    Fr = Fr_list[i]
    Ftheta = Ftheta_list[i]
    t_thrust = t_thrust_list[i]
    s = Spacecraft([0,0,0,0],dt,0,4e5,4000,Fr,Ftheta,t_thrust)
    tmin,dmin = s.min_dist_to_target(Fr,Ftheta,t_thrust,tmax,dt,gdt)
    print("Fr={} Ftheta={} t_thrust={}".format(Fr,Ftheta,t_thrust))
    print("dmin={}, tmin={} Fuel={}"\
      .format(dmin,tmin,(abs(Fr)+abs(Ftheta))*t_thrust))
    s.plot(1,3,plotting[i]);
plt.xlabel('phi',fontsize=20)
plt.ylabel('z',fontsize=20)
plt.plot([0],[0],'r+');
plt.show()

    
