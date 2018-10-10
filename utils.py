import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Road:
    def __init__(self):
        self.numLanes = 2 
        self.laneWidth = 3.7 #meters
        self.length = 80. #meters
        self.fig, self.ax = plt.subplots(1)
        self.startIC = (0,0)
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
        plt.ylim((y - 5, y + self.length + 5))
        plt.xlim((x - 1, x + self.laneWidth * self.numLanes )) 
        plt.axis('equal') 

        
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

    def plot(self):
         x1,y1 = self.start
         self.ax.plot([x1, x1 + self.width], [y1, y1], LineWidth = 3, color = 'w')
         self.ax.plot([x1, x1 + self.width], [y1 + self.height, y1+self.height], LineWidth = 3, color = 'w')

         barWidth = self.width / self.numBars

         for i in range(self.numBars / 2): #numbars over 2 because half are the same color as the road
            rect = patches.Rectangle((x1, y1), barWidth, self.height, facecolor = 'w', linewidth = 0, edgecolor = None)
            self.ax.add_patch(rect)
            x1 += 2 * barWidth



         plt.show()













