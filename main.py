import numpy as np
import matplotlib.pyplot as plt
from utils import *


roadLength = 50
roadFraction = 0.8

road = Road(length = roadLength)
crosswalk = Crosswalk(road, roadFraction = roadFraction) #roadfraction controls where the crosswalk starts
veh = Vehicle(xBrake = roadLength * 0.4, v0 = 15.)
ped = Pedestrian()

sim = Simulation(road, crosswalk, veh, ped, N = 200, ts = 0.1)
out = sim.run()

sim.animate()

# plt.figure()
# plt.plot(out["t"],out["dxP"])
# plt.show()

# plt.figure()
# plt.plot(out["xV"], out["dxVdes"])
# plt.plot(out["xV"], out["dxV"])
# plt.show()

# plt.figure()
# plt.plot(out["t"], out["vehicleState"])
# plt.plot(out["t"], out["pedestrianState"])
# plt.show()

# plt.figure()
# plt.plot(out["xV"], out["ddxV"])
# plt.show()