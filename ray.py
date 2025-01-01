import math
from point import *

class Ray:
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

    def __repr__(self):
        return f'Ray({self.x},{self.y}) with angle {self.angle}'

    def lookAt(self, x, y):
        self.dx = x - self.x
        self.dy = y - self.y
        if self.dx != 0:
            self.angle = -math.atan2(self.dy,self.dx)

    def cast(self, boundary):
        x1 = boundary.x1
        y1 = boundary.y1
        x2 = boundary.x2
        y2 = boundary.y2
        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dx
        y4 = self.y + self.dy
        # denominator
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if 0 <= t <= 1 and u > 0:
            x, y = 0, 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)