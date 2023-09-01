import gravity as gr
import math
import numpy as np
import matplotlib.pyplot as plt

class Spacecraft(gr.Gravity):

      def __init__(self,V0=[0], dt=0.1, t0=0,h=0.0,m=1.0,Fr = 0,Ftheta = 0,t_thrust = 0):
         gr.Gravity.__init__(self,V0, dt, t0, h)
         self.m = m # When F is non null the mass plays a role
         #declare self variables that we will use
         self.Fr = Fr
         self.Ftheta = Ftheta
         self.t_thrust = t_thrust
      def F(self,t,v):
          """ Equation to solve: 
              v[0] is z
              v[1] is dz/dt
              v[2] is phi
              v[3] is dphi/dt
          """
          #when t is larger than tthrust set forces to 0
          if t > self.t_thrust:
              self.Fr = 0
              self.Ftheta = 0
          #copied function from gravity code
          eq1 = v[1]
          eq3 = v[3]
          eq6 = ((-self.G*self.M_E)/(self.r_0 + v[0])**2) + self.Fr/self.m
          eq5 = (self.r_0 + v[0])*((self.omega_0 + v[3])**2)
          eq2 = eq5 + eq6
          eq4 = ((-2*(self.omega_0 + v[3])*v[1])/(self.r_0 + v[0])) + self.Ftheta/(self.m*(self.r_0 + v[0]))
          return(np.array([eq1, eq2, eq3, eq4]))

      def min_dist_to_target(self,Fr,Ftheta,t_thrust,tmax,dt,gdt=1):
        """ Integrate equation and determine min distance to target
          : param Fr     : radial thrust (perpendicular to orbit)
          : param Ftheta : horizontal thrust (parralet to orbit)
          : param t_thrust : duration of thrust
          : param tmax : duration of integration
          : param dt : integration time step
        """
        
        #initial conditions 
        z0 =      -1000
        v_z0 =    0
        phi0=     -2000.0/self.r_0
        v_phi0=   math.sqrt((self.G*self.M_E)/((self.r_0+z0)**3)) - self.omega_0
        #reset class variables to the inital conditions above
        Spacecraft.reset(self,[z0,v_z0,phi0,v_phi0],dt,0) 
        #run function F with the new variables
        self.F(self.t,self.V)
        #iterate with tmax
        self.iterate(tmax)
        #returns minimum distance from gravity module function
        return(self.min_min())

#makes sure that it runs on its own and not twice when called on by another module
if __name__ == '__main__':
    #set conditions
    dt = 0.1
    gdt = 1
    tmax= 4000
    #three conditions we tested first in arrays
    Fr_list = [50,25,10]
    Ftheta_list = [100.,50.,20.]
    t_thrust_list = [100,200,500]
    #colours for plotting
    plotting = ['b-','g-','r-']
    #loops through arrays
    for i in range(len(Fr_list)):
        #i increases by one each time, first,second,third loop
        Fr = Fr_list[i]
        Ftheta = Ftheta_list[i]
        t_thrust = t_thrust_list[i]
        #call class
        s = Spacecraft([0,0,0,0],dt,0,4e5,4000,Fr,Ftheta,t_thrust)
        #print out results
        tmin,dmin = s.min_dist_to_target(Fr,Ftheta,t_thrust,tmax,dt,gdt)
        print("Fr={} Ftheta={} t_thrust={}".format(Fr,Ftheta,t_thrust))
        print("dmin={}, tmin={} Fuel={}"\
          .format(dmin,tmin,(abs(Fr)+abs(Ftheta))*t_thrust))
        #adjust
        plt.subplots_adjust(left=0.15)
        #plots
        s.plot(1,3,plotting[i]);
    #axis labelling and plot
    plt.xlabel('phi(t)',fontsize=20)
    plt.ylabel('z(t)',fontsize=20)
    #our target
    plt.plot([0],[0],'r+');
    plt.legend("abc")
    plt.show()    
