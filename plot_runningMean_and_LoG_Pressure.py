import numpy as np
import matplotlib.pyplot as plt
import os
import re
from LammpsUtilities.convenience import RunningMean, getColorValue

# To make Laplacian of Gaussian and find time when the position drops (Eq. found: https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm)
def LaplaceOfGaussian(x, y, sigma):
	LoG = -1.0/(np.pi * sigma**4) * (1.0-((x**2 + y**2)/(2*sigma**2))) * np.exp(-((x**2 + y**2)/(2*sigma**2)))
	return LoG

# To make legend
def findDriveVelocity(ifilename):
	ifile = open(ifilename)
	fileContent = ifile.read()
	#m = re.search('fix frozen_cube frozen_cube move linear 0 0 ([-]?\d+[\.]?\d*)', fileContent)
	m = re.search('variable pressure equal (\d+[\.]?\d*)', fileContent)
	#print(m.group(1))
	try:
		retVal = float(m.group(1))
	except: 
		retVal = np.nan
	return retVal

# Define how often to smooth
rm2 = RunningMean(1000)

folders_04_10_highPressure = ["04_17_10MPa", "04_17_20MPa", "04_17_30MPa", "04_17_40MPa", "04_17_50MPa", "04_16_60MPa", "04_16_70MPa", "04_16_80MPa_1", "04_23_90MPa", "04_16_100MPa"]
#folders_04_10_highPressure = ["04_17_30MPa", "04_17_20MPa"]

for folder in folders_04_10_highPressure:
	data_distance = np.loadtxt(os.path.join(folder, "cube.z.txt"))
	timestep = data_distance[:,0] - 1000100
	position_high = data_distance[:,2]
	position_low = 21.35
	deltaZ = position_high - position_low
	new_deltaZ = rm2(deltaZ)

	two_water_layer_height = 6.5
	did_reach_below_two_water_layers = np.nanmin(new_deltaZ) < two_water_layer_height
	
	# timestep = timestep[1000:]
	# new_deltaZ = new_deltaZ[1000:]

	time = timestep * (2* 10**-6)

	inputScriptFileName = os.path.join(folder, "system.run")
	driveVelocity = findDriveVelocity(inputScriptFileName)

	if did_reach_below_two_water_layers:
		LoG2 = LaplaceOfGaussian(time, new_deltaZ, 2)
	
		# Find all slope peaks to detect abrupt changes
		LoG_peaks = np.zeros(len(LoG2))
		deltaLoG = np.diff(LoG2)
		deltaT = np.diff(time)
		peaks = np.where(deltaLoG/deltaT > 0.045)
		LoG_peaks[peaks] = LoG2[peaks]

		# for i in range(1, len(LoG2)):
		# 	slope = (LoG2[i]-LoG2[i-1])/(time[i]-time[i-1])
		# 	if slope > 0.045:
		# 		LoG_peaks[i] = LoG2[i]
		
		if np.nansum(LoG_peaks) == 0:
			# Did not find a peak from LoG function, use deltaZ instead
			for i in range(1, len(new_deltaZ)):
				if new_deltaZ[i] < 7:
					slope = (new_deltaZ[i]-new_deltaZ[i-1])/(time[i]-time[i-1])
					if slope > 0.001:
						LoG_peaks[i] = new_deltaZ[i]
						break
	
		maxValue = np.nanmax(LoG_peaks)
		maxIndex = np.nanargmax(LoG_peaks)
		maxTime = time[maxIndex]

		plt.subplot(222)
		plt.title("Pressure vs time for deltaZ drop")
		plt.loglog(driveVelocity, maxTime, '*', label=str(driveVelocity), c=getColorValue(driveVelocity, 10, 100))
		plt.xlabel("log Pressure [MPa]")
		plt.ylabel("log Tau")

		plt.subplot(223)
		plt.title("Time vs Lapacian of Gaussian")
		plt.plot(time, LoG2, label=str(driveVelocity), c=getColorValue(driveVelocity, 20, 100))
		plt.xlabel("Time [ns]")
		plt.ylabel("LoG")
		plt.xlim([0,20])

		plt.subplot(224)
		plt.title("Time vs Peaks from Lapacian of Gaussian")
		plt.plot(time, LoG_peaks, label=str(driveVelocity), c=getColorValue(driveVelocity, 20, 100))
		plt.xlabel("Time [ns]")
		plt.ylabel("LoG peaks")
		plt.xlim([0,20])

	plt.subplot(221)
	plt.title("Pressures from 10-100 MPa")
	plt.plot(time, new_deltaZ, label=str(driveVelocity), c=getColorValue(driveVelocity, 20, 100))
	plt.xlim([0,20])
	plt.xlabel("Time [ns]")
	plt.ylabel("Delta Z [Å]")
	plt.axhline(y=2.75)
	plt.axhline(y=5.5)
	plt.legend()
plt.show()
