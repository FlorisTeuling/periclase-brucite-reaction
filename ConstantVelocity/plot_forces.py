import matplotlib.pyplot as plt
import numpy as np
import os

folders = ["03_23_WithWater_Fram", "03_26_WithWater", "03_22_NoWater"] 
for folder in folders:
	data_forces = np.loadtxt(os.path.join(folder, "forces.txt"))
	timestep = data_forces[:,0]
	fx = data_forces[:,1]
	fy = data_forces[:,2]
	fz = data_forces[:,3]
	Px = (fx * 1.43935*10**-4)*((4.217*9)*(4.217*9))
	Py = (fy * 1.43935*10**-4)*((4.217*9)*(4.217*9))
	Pz = (fz * 1.43935*10**-4)*((4.217*9)*(4.217*9))
	data_distance = np.loadtxt(os.path.join(folder, "cube.z.txt"))
	timestep = data_distance[:,0]
	deltaZ = data_distance[:,3]
	deltaZ = deltaZ  - 2.5
	plt.figure()
	plt.plot(deltaZ, Pz)
	plt.xlabel("DeltaZ (Å)")
	plt.ylabel("Pressure (MPa)")
	plt.xlim([-5,30])
plt.show()

