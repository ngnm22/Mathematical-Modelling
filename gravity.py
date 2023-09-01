from ode_rk4 import *
import math
import numpy as np
class Gravity(ODE_RK4):
  def __init__(self,V0=[0], dt=0.1, t0=0,h=0.0):
      """ V0 : initial conditions for z, v_z, phi, v_phi.
          dt : integration time step
          t0 : initial time
          h : altitude of the target orbit
      """
      super().__init__(V0,dt,t0)
      self.h = h
      self.G = 6.673e-11
      self.M_E = 5.97e24
      self.R_E = 6370e3
      self.r_0 = self.R_E+h
      self.omega_0 = math.sqrt(self.G*self.M_E/self.r_0**3)
      self.F_r = 0
      self.F_theta = 0
      self.m = 1
      self.t_last = 0
      self.d_last = -1
      self.d_butlast = -1
      self.d_min = []
      self.d_max = []

  def reset(self, V0, dt, t0=0):
      """ Reset the integration parameters; see __init__ for more info."""
      super().reset(V0, dt, t0)
      self.t_last = 0
      self.d_last = -1
      self.d_butlast = -1
      self.d_min = []
      self.d_max = []

    
      
  def F(self,t,v):
      """ Equation to solve: 
          v[0] is z
          v[1] is dz/dt
          v[2] is phi
          v[3] is dphi/dt
      """
      #below shows our 4 first order differential eqs
      eq1 = v[1]
      eq3 = v[3]
      eq6 = ((-self.G*self.M_E)/(self.r_0 + v[0])**2) + self.F_r/self.m
      eq5 = (self.r_0 + v[0])*((self.omega_0 + v[3])**2)
      #I have broken down dz/dt for checking purposes but all lines out in the end
      eq2 = eq5 + eq6
      eq4 = ((-2*(self.omega_0 + v[3])*v[1])/(self.r_0 + v[0])) + self.F_theta/(self.m*(self.r_0 + v[0]))
      #returns an array of these eqs
      return(np.array([eq1, eq2, eq3, eq4]))

  def dist_2_reference(self):
      #put in the distance needed to be found for polar co ordinates
      self.d_curr = math.sqrt((2*self.r_0)*(1 - np.cos(self.V[2]))*(self.r_0+self.V[0]) + self.V[0]**2)
      #returning distance
      return(self.d_curr)

  def post_integration_step(self):
      #calling the function to calculate distance
      self.dist_2_reference()
      if self.d_last >=0 and self.d_butlast >= 0:
          #we can start finding minimum once we know distances used arent 0
          if self.d_last < self.d_curr and self.d_last < self.d_butlast:
              #outlining conditions for identifying a minimum, where the middle value in an
              #array of 3 needs to be smaller than the rest.
              self.d_min.append([self.t_last,self.d_last])
              #adding minimum distance and its time to the array
      #changing values so that the next values can be used in the next loop
      self.d_butlast = self.d_last
      self.d_last = self.d_curr
      self.t_last = self.t
      #return array of the minimum distances
      return(self.d_min)
      
      
  def min_min(self,t_after=0):
      #call the array of minimum distances
      self.post_integration_step()
      #make sure there is a minimum distance to test
      #ignoring all the minima before tafter
      if self.t > t_after and self.d_min != []:
          #find the minimum value for dmin in the array
          index = np.argmin(self.d_min,axis = 0)
          #return minimum distance
          return(self.d_min[index[1]])

