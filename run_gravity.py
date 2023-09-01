import gravity
import matplotlib.pyplot as plt
import math


h = 5e5 # Altitude of reference trajectory
eq = gravity.Gravity([0,0,0,0],0.1,0,h) # Create gravity instance

# Perform the integration for the given initial conditions
# Integrate up to t=12000s and produeces 3 figues, z(t), phi(t) and z(phi)
# z0,v_z0,phi0,v_phi0: initial values for the functions
def run(scenario,z0,v_z0,phi0,v_phi0):
    # integration parameters
    t0 = 0
    dt = 0.1
    t_max = 12000
    dt_grf = 10
    eq.reset([z0,v_z0,phi0,v_phi0],dt,t0) 
    # Display initial condition on screen
    print("Scenario {}:".format(scenario))
    print("t={}  z={} dz/dt={} phi={} dphi/dt={} "\
        .format(eq.t,eq.V[0],eq.V[1],eq.V[2],eq.V[3],))
    # Integrate until t_max
    eq.iterate(t_max,dt_grf) 
    
    # Display position after integration
    print("t={}  z={} dz/dt={} phi={} dphi/dt={} "\
        .format(eq.t,eq.V[0],eq.V[1],eq.V[2],eq.V[3],))
    # Plot z(t)
    plt.xlabel('t',fontsize=20)
    plt.ylabel('z',fontsize=20)
    plt.subplots_adjust(left=0.15)
    eq.plot(1, 0, "-b")
    plt.show() 
    # Plot phi(t)
    plt.xlabel('t',fontsize=20)
    plt.ylabel('phi',fontsize=20)
    plt.subplots_adjust(left=0.15)
    eq.plot(3, 0, "-r")
    plt.show()
    # Plot z(phi)
    plt.xlabel('phi',fontsize=20)
    plt.ylabel('z',fontsize=20)
    plt.subplots_adjust(left=0.15)
    eq.plot(1, 3, "-k")
    plt.show()

# Scenario a
G = 6.673e-11
M_E = 5.97e24
R_E = 6370e3
r_0 = R_E+h
omega_0 = math.sqrt(G*M_E/r_0**3)
z0 =      0
v_z0 =    0
phi0=     0
v_phi0=  0
run("a",z0,v_z0,phi0,v_phi0)

# Scenario b
z0 = 1000.
v_z0=0.
phi0 = 0.
v_phi0 = math.sqrt(eq.G*eq.M_E/(eq.r_0+z0)**3)-eq.omega_0
run("b",z0,v_z0,phi0,v_phi0)

# Scenario c
z0 = 0.
v_z0= 0.
phi0 = 0.
v_phi0 = 100./(eq.r_0+z0)
run("c",z0,v_z0,phi0,v_phi0)


