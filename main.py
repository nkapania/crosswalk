import numpy as np
import matplotlib.pyplot as plt
from utils import *


roadLength = 100
roadFraction = 0.8

road = Road(length = roadLength)
crosswalk = Crosswalk(road, roadFraction = roadFraction) #roadfraction controls where the crosswalk starts
veh = Vehicle(xBrake = roadLength * 0.2, crosswalk = crosswalk, v0 = 15.)
ped = Pedestrian()

sim = Simulation(road, crosswalk, veh, ped, N = 200, ts = 0.1)
out = sim.run()

#sim.animate()
plotThings = True


if plotThings:

	x = out["t"]
	#x = out["xV"]

	plt.figure()
	plt.plot(x,out["dxP"])
	plt.xlabel('time (s)')
	plt.ylabel('Pedestrian Velocity (m/s)')

	plt.figure()
	plt.plot(x, out["dxVdes"], label = "Desired Velocity")
	plt.plot(x, out["dxV"], label = "Actual Velocity")
	plt.xlabel('time(s)')
	plt.legend()
	plt.ylabel('Vehicle Velocity')

	plt.figure()
	plt.plot(x, out["vehicleState"], label = "Vehicle State")
	plt.plot(x, out["pedestrianState"], label = "Pedestrian State")
	plt.xlabel('time(s)')
	plt.ylabel('State Machine State')
	plt.legend()

	plt.figure()
	plt.plot(x, out["ddxV"], label = "Vehicle Acceleration")
	plt.xlabel('time(s)')
	plt.ylabel('Vehicle Acceleration')
	# plt.legend()
	plt.show()