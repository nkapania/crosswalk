import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation

class Road:
    def __init__(self, length = 80):
        
        x0 = 0
        y0 = 0 #start at origin
        self.numLanes = 4 
        self.laneWidth = 3.7 #meters
        self.length = length #meters
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
                if i == 1: #median
                    plt.plot([x, x], [y, y + self.length],color = 'y',LineStyle = '-', LineWidth = 3)
                else:
                    plt.plot([x, x], [y, y + self.length],color = 'w',LineStyle = '--', LineWidth = 3)

        
        x0,y0 = self.startIC
        self.ax.axis('equal') 
        self.ax.set_ylim([y - 5, y + self.length + 5])
        self.ax.set_xlim([x - 1, x + self.laneWidth * self.numLanes]) 
        
class Crosswalk:
    def __init__(self, road, roadFraction = 0.5):
        self.width = road.numLanes * road.laneWidth
        self.height = 3.0 #meters
        self.fig = road.fig
        self.ax  = road.ax
        self.numBars = road.numLanes * 4 #number of bars on crosswalk for graphical purposes
        self.roadFraction = roadFraction

        x,y = road.startIC
        self.start = (x, y + road.length * self.roadFraction)
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
    #cY = y coordinate of crosswalk
    def __init__(self, xBrake, v0 = 20):
        self.m = 1500. #kg
        self.v0 = v0
        self.lane = 2 # lane 2 corresponds to third lane from the left
        self.width = 1.5 #meters
        self.height = 2.5 #meters
        self.state = "driving"
        self.kSpeed = 3.
        self.xBrake =  xBrake #position to start braking the car 

    def getAccel(self, xP, dxP, xV, dxV, t, crosswalk):
        accel = self.getAccelStateMachine(xP, dxP, xV, dxV, t, crosswalk)
        return accel

    def getAccelStateMachine(self, xP, dxP, xV, dxV, t, crosswalk):
        if self.state == "driving":
            dxVdes = self.v0
            accel = self.kSpeed*(dxVdes - dxV)
            state = 0

            #check if pedestrian in crosswalk
            if xP > 0 and xP < crosswalk.width:
                self.state = "braking"

        elif self.state == "braking":
            xStop = crosswalk.start[1] - self.height * 2 #give buffer for vehicle stop

            if xV < self.xBrake:
                dxVdes = self.v0  #before brakepoint - keep driving!

            elif xV > xStop:
                dxVdes = 0. #past the crosswalk, desired speed is 0

            else:
                dxVdes = self.v0 - self.v0 / (xStop - self.xBrake) * (xV - self.xBrake)
            

            accel = self.kSpeed*(dxVdes - dxV)
            state = 1

            if xP > crosswalk.width:
                self.state = "driving"

        return accel, state, dxVdes



class Pedestrian:
    def __init__(self, v0 = 0):
        self.m = 50. #kg
        self.v0 = v0
        self.radius = 1. #m
        self.state = "waiting" #possible states are "waiting"
        self.waitTime = 0.5 #number of seconds pedestrian takes to gauge situation
        self.kSpeed = 10 #m/s2 per m/s of error
        self.vDes = 1.2 #m/s
        self.minGap = 30. #m

    def getAccel(self, xP, dxP, xV, t, crosswalk):
        accel = self.getAccelStateMachine(xP, dxP, xV, t, crosswalk)
        return accel

    def getAccelStateMachine(self, xP, dxP, xV, t, crosswalk):
        gap = self.calculateGap(xV, crosswalk)
        if self.state == "waiting":
            if t > self.waitTime and gap > self.minGap:
                self.state = "walking"

            state = 0
            accel = 0
        elif self.state == "walking":
            accel = self.kSpeed * (self.vDes - dxP)
            state = 1

        return accel, state, gap

    def calculateGap(self,xV, crosswalk):
        gap = crosswalk.start[1] - xV
        #car is past the crosswalk
        if gap < 0:
            gap = 99999.

        return gap


#Simulate with double euler integration
class Simulation:
    def __init__(self, road, crosswalk, vehicle, pedestrian, ts = 0.1, N = 100):
        self.ts = ts #seconds
        self.N = N #number of time steps to simulate
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
        ddxV = np.zeros(dxV.shape)

        #pedestrian motion
        xP = np.zeros((self.N, 1))
        dxP = np.zeros(xP.shape); dxP[0] = self.pedestrian.v0
        ddxP = np.zeros(xP.shape)

        pedestrianState =  np.zeros(xP.shape)
        vehicleState = np.zeros(xP.shape)
        gap = np.zeros(xP.shape)
        dxVdes = np.zeros(xP.shape)


        #other arrays
        t = np.zeros((self.N, 1))

        #main loop

        for i in range(1, self.N):
            t[i] = t[i-1] + self.ts

            ddxV[i], vehicleState[i], dxVdes[i] = self.vehicle.getAccel(xP[i-1], dxP[i-1], xV[i-1], dxV[i-1], t[i-1], self.crosswalk)
            ddxP[i], pedestrianState[i], gap[i] = self.pedestrian.getAccel(xP[i-1], dxP[i-1], xV[i-1], t[i-1], self.crosswalk)

            dxV[i] = self.ts * ddxV[i] + dxV[i-1]
            dxP[i] = self.ts * ddxP[i] + dxP[i-1]

            xV[i] = self.ts * dxV[i] + xV[i-1]
            xP[i] = self.ts * dxP[i] + xP[i-1]


        self.out = {'t': t, 'xV': xV, 'dxV': dxV, 'ddxV': ddxV, 'xP': xP, 'dxP': dxP, 'ddxP': ddxP,
        'pedestrianState': pedestrianState, 'vehicleState': vehicleState, 'dxVdes': dxVdes}

        return self.out


    def animate(self):
        #get up to date axis with road and crosswalk plotted
        fig,ax  = self.crosswalk.getAxis()

        #unpack arrays
        xP = self.out["xP"]
        xV = self.out["xV"]

        #plot vehicle
        vehicle    = patches.Rectangle((0, 0), 0, 0, fc='k')
        pedestrian = patches.Rectangle((0, 0), 0, 0, fc='r')
        
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
        













    












