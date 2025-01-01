import math
from ray import *

class Point:
    def __init__(self, x, y, label=None):
        self.x = x
        self.y = y
        self.label = label

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other):
        # check for their approximate position
        if isinstance(other, Point):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __hash__(self):
        return hash(f'Point({round(self.x)}, {round(self.y)})')

    def dist(self, other):
        if isinstance(other, Point):
            return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

    def isvisible(self, other, bounds):
        ray = Ray(other.x, other.y, self.angleto(other))
        closestPt = other
        closestDist = self.dist(other)
        # cast a ray from the other point in the direction of this point
        # if there is a new point between this point and the other point, it's not visible
        for bound in bounds:
            # ignore the wall if self is an endpoint
            # if self in bound.points:
            #     continue
            pt = ray.cast(bound)
            if pt:
                intPt = Point(pt[0], pt[1])
                # if the intersection point is the same point as the one we're checking, ignore it
                if math.isclose(self.x, intPt.x) and math.isclose(self.y, intPt.y):
                    continue
                if other.dist(intPt) < closestDist:
                    closestPt = intPt
                    closestDist = other.dist(intPt)
        if closestDist < self.dist(other):
            return False
        return True

    def angleto(self, other):
        if isinstance(other, Point):
            angle = math.atan2(self.y - other.y, self.x - other.x)
            return angle if angle > 0 else angle + 2 * math.pi

    def angleto2(self, other):
        if isinstance(other, Point):
            angle = math.atan2(self.y - other.y, self.x - other.x)
            return abs(angle)
