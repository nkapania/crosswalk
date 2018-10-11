import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

class Road:
    def __init__(self):
        
        x0 = 0
        y0 = 0 #start at origin
        self.numLanes = 4 
        self.laneWidth = 3.7 #meters
        self.length = 80. #meters
        self.fig, self.ax = plt.subplots(1)
        self.startIC = (x0,y0)
        self.color = '#949392' #light grey
        self.plot()
        


    def plot(self):
        x, y = self.startIC

        for i in range(self.numLanes):
            rect = patches.Rectangle((x,y), self.laneWidth, self.length, facecolor = self.color, linewidth = 0, edgecolor = None, linestyle = '--')
            self.ax.add_patch(rect)
            x += self.laneWidth

            if i < self.numLanes - 1:
                plt.plot([x, x], [y, y + self.length],color = 'w',LineStyle = '--', LineWidth = 3)
        
        x0,y0 = self.startIC
        self.ax.axis('equal') 
        self.ax.set_ylim([y - 5, y + self.length + 5])
        self.ax.set_xlim([x - 1, x + self.laneWidth * self.numLanes]) 
        
class Crosswalk:
    def __init__(self, road):
        self.width = road.numLanes * road.laneWidth
        self.height = 3.0 #meters
        self.fig = road.fig
        self.ax  = road.ax
        self.numBars = road.numLanes * 4 #number of bars on crosswalk for graphical purposes

        x,y = road.startIC
        self.start = (x, y + road.length * .67)
        self.plot()

    def getAxis(self):
        return self.fig, self.ax

    def plot(self):
        x1,y1 = self.start
        self.ax.plot([x1, x1 + self.width], [y1, y1], LineWidth = 3, color = 'w')
        self.ax.plot([x1, x1 + self.width], [y1 + self.height, y1+self.height], LineWidth = 3, color = 'w')

        barWidth = self.width / self.numBars

        for i in range(self.numBars / 2): #numbars over 2 because half are the same color as the road
            rect = patches.Rectangle((x1, y1), barWidth, self.height, facecolor = 'w', linewidth = 0, edgecolor = None)
            self.ax.add_patch(rect)
            x1 += 2 * barWidth

class Vehicle:
    def __init__(self, v0 = 20):
        self.m = 1500. #kg
        self.v0 = v0
        self.lane = 2 # lane 2 corresponds to third lane from the left
        self.width = 1.5 #meters
        self.height = 2.5 #meters

    def getAccel(self):
        accel = 0
        return accel

class Pedestrian:
    def __init__(self, v0 = 1.2):
        self.m = 50. #kg
        self.v0 = v0
        self.radius = 1. #m

    def getAccel(self):
        accel = np.random.randn()
        return accel


#Simulate with double euler integration
class Simulation:
    def __init__(self, road, crosswalk, vehicle, pedestrian):
        self.ts = 0.1 #seconds
        self.N = 100 #number of time steps to simulate
        self.vehicle = vehicle
        self.road = road
        self.pedestrian = pedestrian
        self.crosswalk = crosswalk
        self.out = {}

    def run(self):

        #Initialize arrays

        #vehicle motion
        xV = np.zeros((self.N, 1))
        dxV = np.zeros(xV.shape); dxV[0] = self.vehicle.v0
        ddxV = np.zeros(dxV.shape);

        #pedestrian motion
        xP = np.zeros((self.N, 1))
        dxP = np.zeros(xP.shape); dxP[0] = self.pedestrian.v0
        ddxP = np.zeros(xP.shape)

        #other arrays
        t = np.zeros((self.N, 1))

        #main loop

        for i in range(1, self.N):
            t[i] = t[i-1] + self.ts

            ddxV[i] = self.vehicle.getAccel()
            ddxP[i] = self.pedestrian.getAccel()

            dxV[i] = self.ts * ddxV[i] + dxV[i-1]
            dxP[i] = self.ts * ddxP[i] + dxP[i-1]

            xV[i] = self.ts * dxV[i] + xV[i-1]
            xP[i] = self.ts * dxP[i] + xP[i-1]


        self.out = {'t': t, 'xV': xV, 'dxV': dxV, 'ddxV': ddxV, 'xP': xP, 'dxP': dxP, 'ddxP': ddxP}

        return self.out


    def animate(self):
        #get up to date axis with road and crosswalk plotted
        fig,ax  = self.crosswalk.getAxis()

        #unpack arrays
        xP = self.out["xP"]
        xV = self.out["xV"]

        #plot vehicle
        vehicle    = patches.Rectangle((0, 0), 0, 0, fc='y')
        pedestrian = patches.Rectangle((0, 0), 0, 0, fc='g')
        
        vehicleX = self.vehicle.lane * self.road.laneWidth + self.road.laneWidth / 2 - self.vehicle.width/2
        pedestrianY = self.crosswalk.start[1]


        def init():
            ax.add_patch(vehicle)
            ax.add_patch(pedestrian)
            return vehicle, pedestrian

        def animate(i):

            vehicle.set_width(self.vehicle.width)
            vehicle.set_height(self.vehicle.height)
            vehicle.set_xy([vehicleX, xV[i]]) #Note that xV is vertical for the car

            pedestrian.set_width(self.pedestrian.radius)
            pedestrian.set_height(self.pedestrian.radius)
            pedestrian.set_xy([xP[i] ,pedestrianY]) 

            return vehicle, pedestrian

        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(xV), interval=100, blit=True)
        plt.show()        






# def initAnimation():
#     ax.add_patch(vehiclePatch)
#     return vehiclePatch

# def animate(i):
#     patch.set_width(1.5) #hardcoded
        













    












