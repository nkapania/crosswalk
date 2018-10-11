import numpy as np
import matplotlib.pyplot as plt
from utils import *

road = Road()
crosswalk = Crosswalk(road)
veh = Vehicle()
ped = Pedestrian()

sim = Simulation(road, crosswalk, veh, ped)
out = sim.run()

sim.animate()

# plt.figure()
# plt.plot(out["t"],out["xP"])
# plt.show()

