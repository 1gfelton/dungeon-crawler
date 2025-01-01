import math
from ray import *
from point import *

class Particle:
    def __init__(self, x, y, direction=90):
        self.x, self.y = x, y
        self.direction = (direction + 360) % 360
        self.rays = []
        self.fov = 35
        self.numRays = 100
        self.enemies = []
        self.items = []
        self.startAng = self.direction - self.fov/2
        for i in range(0, self.numRays, 1):
            angle = self.startAng + (i * self.fov / self.numRays)
            angle = (angle + 360) % 360
            self.rays.append(Ray(self.x, self.y, math.radians(angle)))

    def __repr__(self):
        return f'Particle({self.x}, {self.y}) with {len(self.rays)} rays'

    def rotate(self, dir):
        for i in range(len(self.rays)):
            curr = self.rays[i]
            curr.angle += dir

    def recalc(self):
        self.rays = []
        for i in range(0, self.numRays, 1):
            self.rays.append(Ray(self.x, self.y, math.radians(self.direction + (self.fov/self.numRays * i))))

    def cast(self, bounds):
        points = dict()
        for ray in self.rays:
            record = math.inf
            best = None
            seen = []
            closestEnemyDist = math.inf
            closeEnemy = None
            closestItemDist = math.inf
            closeItem = None
            for bound in bounds:
                intersect = ray.cast(bound)
                if intersect:
                    pt = Point(intersect[0], intersect[1])
                    d = pt.dist(Point(self.x, self.y))
                    if d < record:
                        record = d
                        best = pt
            # find the enemies in the fov
            for enemy in self.enemies:
                if enemy not in seen:
                    enemyPoint = Point(enemy.x, enemy.y)
                    a = math.atan2(self.y - enemy.y, self.x - enemy.x)
                    angle_from_enemy = a if a >= 0 else a + 2*math.pi
                    d = enemyPoint.dist(Point(self.x, self.y))
                    fov = math.radians(self.fov)
                    if abs(ray.angle - angle_from_enemy) < fov / 2:
                        dist = Point(self.x, self.y).dist(enemyPoint)
                        if dist < record:
                            closeEnemy = enemy
                            closestEnemyDist = dist
            if closeEnemy:
                seen.append(closeEnemy)
                points[closestEnemyDist] = closeEnemy
            for item in self.items:
                if item not in seen:
                    itemPoint = Point(item.x, item.y)
                    a = math.atan2(self.y - item.y, self.x - item.x)
                    angleFromItem = a if a >= 0 else a + 2*math.pi
                    d = itemPoint.dist(Point(self.x, self.y))
                    fov = math.radians(self.fov)
                    if abs(ray.angle - angleFromItem) < fov / 2:
                        dist = Point(self.x, self.y).dist(itemPoint)
                        if dist < record:
                            closeItem = item
                            closestItemDist = dist
            if closeItem:
                seen.append(closeItem)
                points[closestItemDist] = closeItem
            if best:
                dist = best.dist(Point(self.x, self.y))
                points[dist] = best
        return points

    def normalizeDir(self):
        self.direction = (self.direction + 360) % 360