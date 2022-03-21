#ENCH 519 - Assignment 2
#Problem: Simulate the ODE: taup * d(Delta*T)/dt + Delta*T = (Tinf - T0)
#Plot response to square wave inpout wqtih f = 4 and tspan = 1.75

#IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import signal

#CONSTANTS AND TIME SAMPLING ARRAY
cv = 140 #Heat capacity of Mercury in J/(kG K)
m = 0.7e-3 #Mass of Hg in the Thermometer (kg)
T0 = 293.15 #Initial temperature of the thermometer (K)
Tinf = 310.15 #Initial temperature of the water (K)
As = 0.001610066 #Surface area for a thermometer that is 10cm deep and .5cm in diameter (m^2)
h = 250.0 #Convective heat transfer coefficient between water and thermometer (W/(m^2 K))
Kp = (Tinf - T0)
taup = (m*cv)/(h*As)
t = np.linspace(0, 30, 500, endpoint=False) #input time array. 500Hz sampling over 1.75 second span

#RHS OF ODE
def f(t, y):
  dydt = (Kp*Square(t) - y) / taup
  return dydt

#SQUARE WAVE FUNCTION
def Square(t):
    #t=np.linspace(0,1.75,4,endpoint=True)
    signal.square(2*np.pi*0.002*t) #frequency = 4/s     
    return signal.square(2*np.pi*0.002*t)    

#TIME SPANS, INITIAL VALUES, AND CONSTANTS
tspan = np.linspace(0, 30)
yinit = [0]

#SOLVE ODE
sol = solve_ivp(lambda t, y: f(t, y), #recall: f is the RHS of the ODE
                [tspan[0], tspan[-1]], yinit, method='RK45', t_eval=tspan)

#Ensuring bulb temperature never goes above that of the surroundings:
for i in range(0,len(sol.t)):
 if sol.y[0][i] > (Tinf - T0):
    sol.y[0][i] = (Tinf - T0)

#PLOTTING ODE SOLUTION
plt.figure(1)
plt.title("First-order Response to a Square Wave Input")
plt.plot(t, signal.square(2*np.pi*4*t),label='Square Wave Func') 
plt.plot(sol.t,sol.y[0],'r-',linewidth=1,label='ODE Solution')
plt.xlabel('Time (s)')
plt.ylabel('Temperature change of thermometer (K)')
plt.legend(loc='best')
plt.show()

#PLOTTING SQUARE WAVE INPUT
plt.plot(t, signal.square(2*np.pi*4*t))
plt.title("Square Wave Function") 
plt.xlabel('Time (s)')
plt.ylabel('Square Wave Output')
plt.legend(loc='best')
plt.show()
