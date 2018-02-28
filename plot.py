import matplotlib.pyplot as plt
import numpy as np
import os

data = np.loadtxt("cube.z.txt")
timestep = data[:,0]
pressure = data[:,1]
deltaZ = data[:,4]

plt.figure()
plt.plot(pressure, deltaZ)
plt.xlabel("Pressure [MPa]")
plt.ylabel("Delta z (Å)")
plt.legend()
plt.show()