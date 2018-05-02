import numpy as np
import matplotlib.pyplot as plt
import os
import re
from LammpsUtilities.convenience import RunningMean, getColorValue

# To make Laplacian of Gaussian and find time when the position drops (Eq. found: https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm)
def LaplaceOfGaussian(x, y, sigma):
	LoG = -1/(np.pi * sigma**4) * (1-((x**2 + y**2)/sigma**2)) * np.exp(-((x**2 + y**2)/(2*sigma**2)))
	return LoG

# To make legend
def findAngle(ifilename):
	ifile = open(ifilename)
	fileContent = ifile.read()
	m = re.search('angle = (\d+[\.]?\d*)', fileContent)
	#print(m.group(1))
	try:
		retVal = float(m.group(1))
	except: 
		retVal = np.nan
	return retVal


# Define how often to smooth
rm1 = RunningMean(500)

folders_changeAngle = ["Angle0/Pressure30MPa","Angle11.25/Pressure30MPa", "Angle16.875/Pressure30MPa", "Angle22.5/Pressure30MPa", "Angle28.125/Pressure30MPa", "Angle33.75/Pressure30MPa","Angle39.375/Pressure30MPa", "Angle45/Pressure30MPa"]
#folders_changeAngle = ["Angle22.5/Pressure30MPa"]
for folder in folders_changeAngle:
	data_distance = np.loadtxt(os.path.join(folder, "cube.z.txt"))
	timestep = data_distance[:,0] - 1000100 
	position_high = data_distance[:,2]
	position_low = 21.35
	deltaZ = position_high - position_low
	new_deltaZ = rm1(deltaZ)

	timestep = timestep[1000:]
	new_deltaZ = new_deltaZ[1000:]

	time = timestep * (2 * 10**-6) 

	inputScriptFileName = os.path.join(folder, "../MakeInput/create_slab_with_water_cubeOrintation.py")
	angle = findAngle(inputScriptFileName)

	LoG2 = LaplaceOfGaussian(time, new_deltaZ, 2)
	
	a = np.zeros(len(LoG2))
	for i in range(0, len(LoG2)-1):
		if (LoG2[i]-LoG2[i-1])/(time[i]-time[i-1]) > 0.045:
			a[i] = LoG2[i]

	if np.nansum(a) == 0:
		a = LoG2


	maxValue = np.nanmax(a)
	maxIndex = np.nanargmax(a)
	maxTime = time[maxIndex]

	plt.subplot(222)
	plt.title("Angle vs time for deltaZ drop")
	plt.plot(angle, maxTime, '*', label=str(angle), c=getColorValue(angle, 0, 45))
	plt.xlabel("Angle")
	plt.ylabel("Tau")

	plt.subplot(221)
	plt.title("Constant Pressure 30 MPa, Changing Angle")
	plt.plot(time, new_deltaZ, label=str(angle), c=getColorValue(angle, 0, 45))
	plt.xlim([0,10])
	plt.xlabel("Time [ns]")
	plt.ylabel("Delta Z [Å]")
	plt.axhline(y=2.75)
	plt.axhline(y=5.5)
	plt.legend()

	plt.subplot(223)
	plt.title("Time vs Lapacian of Gaussian")
	plt.plot(time, LoG2, label=str(angle), c=getColorValue(angle, 0, 45))
	plt.xlabel("Time [ns]")
	plt.ylabel("LoG")
	plt.xlim([0,10])

	plt.subplot(224)
	plt.title("Time vs Peaks from Lapacian of Gaussian")
	plt.plot(time, a, label=str(angle), c=getColorValue(angle, 0, 45))
	plt.xlabel("Time [ns]")
	plt.ylabel("LoG peaks")
	plt.xlim([0,10])
plt.show()
