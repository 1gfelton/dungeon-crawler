from point import *

class Boundary:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.points = [Point(x1, y1), Point(x2, y2)]

    def __repr__(self):
        return f'Boundary(({self.x1, self.y1}),({self.x2, self.y2}))'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Boundary):
            return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2

    def isIntersecting(self, boundary):
        if isinstance(boundary, Boundary):
            x1 = boundary.x1
            y1 = boundary.y1
            x2 = boundary.x2
            y2 = boundary.y2
            x3 = self.x1
            y3 = self.y1
            x4 = self.x2
            y4 = self.y2
            # denominator
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                return
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            if 0 <= t <= 1 and 0 <= u <= 1:
                pt = Point(0, 0)
                pt.x = x1 + t * (x2 - x1)
                pt.y = y1 + t * (y2 - y1)
                return pt