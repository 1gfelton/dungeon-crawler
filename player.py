from cmu_graphics import *
import math
from boundary import Boundary
from item import *
from ray import *
from point import *
from button import *

class Player:
    def __init__(self, x, y, direction=90):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.health = 100
        self.armor = 0.0
        self.sprite = None
        self.size = 5
        self.inventory = dict()
        self.velocity = 1
        self.currentItem = None
        self.direction = math.radians(direction)

    def __repr__(self):
        return f'Player at {self.x}, {self.y}'

    def draw(self):
        drawCircle(app.player.x, app.player.y, app.player.size, fill='red')
        playerHealth = HealthBar('Player Health', self.x, self.y - 20, 40, 10, '', self.health)
        playerHealth.draw()
        # drawLabel(f'Player with {self.health} health', self.x, self.y - 20)

    def isColliding(self, other):
        if isinstance(other, Item):
            if ((other.bottomBound >= self.y >= other.topBound) and
                (other.leftBound <= self.x <= other.rightBound)):
                return True
        elif isinstance(other, Boundary):
            if self.distanceToWall(other) < self.size:
                return True
        elif isinstance(other, Enemy):
            if distance(self.x, self.y, other.x, other.y) <= self.size*2:
                return True
        return False

    def pickupItem(self, other):
        if isinstance(other, Item):
            other.size = 10
            self.inventory[other.name] = other

    def checkBounds(self, appWidth, appHeight):
        if self.x-self.size <= 0:
            self.x = self.size
        elif self.x+self.size >= appWidth:
            self.x = appWidth-self.size
        elif self.y-self.size <= 0:
            self.y = 0+self.size
        elif self.y+self.size >= appHeight:
            self.y = appHeight-self.size

    def distanceToWall(self, boundary):
        # match wikipedia distance from line to point formula https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        x0, y0 = self.x, self.y
        x1, y1, x2, y2 = boundary.x1, boundary.y1, boundary.x2, boundary.y2
        den = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        return num / den

    def getClosestWall(self, walls):
        record = math.inf
        wallDist = dict()
        for wall in walls:
            result = self.distanceToWall(wall)
            wallDist[result] = wall
            record = min(result, record)
        return wallDist[record]

    def isVisible(self, other, walls):
        ray = Ray(self.x, self.y, self.getDirectionTo(other))
        player = Point(self.x, self.y)
        otherPos = Point(other.x, other.y)
        for wall in walls:
            int = ray.cast(wall)
            if int:
                pt = Point(int[0], int[1])
                if pt.dist(player) < player.dist(otherPos):
                    return False
        return True

    def getDirectionTo(self, other):
        if (isinstance(other, Item) or
            isinstance(other, Boundary) or
            isinstance(other, Enemy) or
            isinstance(other, Player)):
            x0, x1 = self.x, other.x
            y0, y1 = self.y, other.y
            return math.atan2(y1 - y0, x1 - x0)

class Enemy(Player):
    def __init__(self, x, y, name, url=''):
        self.name = name
        self.anatomy = dict()
        self.url = url
        for hitbox in {'Head','Left','Right','Chest'}:
            self.anatomy[hitbox] = [100]
        super().__init__(x, y)

    def draw(self):
        assert(self.size > 0)
        drawStar(self.x, self.y, self.size, 5)
        drawLabel(f'Enemy {self.name}, health: {self.health}', self.x, self.y - 20)

    def __repr__(self):
        return f'Enemy {self.name} at {self.x}, {self.y}, {self.health} hp'

    def seek(self, player):
        if isinstance(player, Player):
            for i in range(10):
                x0, y0 = self.x, self.y
                x1, y1 = player.x, player.y
                angle = self.getDirectionTo(player)
                self.dx, self.dy = x1-x0, y1-y0
                self.x += 1/self.dx
                self.y += 1/self.dy