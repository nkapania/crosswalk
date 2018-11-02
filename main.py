import numpy as np
import matplotlib.pyplot as plt
from utils import *


NUM_SIMULATIONS = 10
roadLength = 100.

for i in range(NUM_SIMULATIONS):

	roadFraction = np.random.rand()

	road = Road(length = roadLength)
	crosswalk = Crosswalk(road, roadFraction = roadFraction) 
	veh = Vehicle(crosswalk = crosswalk, v0 = 15.)
	ped = Pedestrian(crosswalk, minGap = 2.0, start = "right")

	sim = Simulation(road, crosswalk, veh, ped, N = 200, ts = 0.1)
	out = sim.run()

	sim.animate()
	#plotThings = True





# if plotThings:

# 	x = out["t"]
# 	xlabel = 'time (s)'

# 	# x = out["xV"]
# 	# xlabel = 's (m)'

# 	plt.figure()
# 	plt.plot(x,out["dxP"])
# 	plt.xlabel(xlabel)
# 	plt.ylabel('Pedestrian Velocity (m/s)')

# 	plt.figure()
# 	plt.plot(x, out["dxVdes"], label = "Desired Velocity")
# 	plt.plot(x, out["dxV"], label = "Actual Velocity")
# 	plt.xlabel(xlabel)
# 	plt.legend()
# 	plt.ylabel('Vehicle Velocity')

# 	plt.figure()
# 	plt.plot(x, out["vehicleState"], label = "Vehicle State")
# 	plt.plot(x, out["pedestrianState"], label = "Pedestrian State")
# 	plt.xlabel(xlabel)
# 	plt.ylabel('State Machine State')
# 	plt.legend()

# 	plt.figure()
# 	plt.plot(x, out["xV"], label = "Vehicle Position")
# 	plt.xlabel(xlabel)
# 	plt.ylabel('Position (m)')
# 	plt.legend()

# 	plt.figure()
# 	plt.plot(x, out["ddxV"], label = "Vehicle Acceleration")
# 	plt.xlabel(xlabel)
# 	plt.ylabel('Vehicle Acceleration')
# 	# plt.legend()
# 	plt.show()