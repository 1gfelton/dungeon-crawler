from cmu_graphics import *
class Item:
    def __init__(self, name, x, y, size, color='black', url=''):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.leftBound = self.x
        self.topBound = self.y
        self.rightBound = self.x + self.size
        self.bottomBound = self.y + self.size
        self.color = color
        self.url = url
        self.drawSize = 35
        self.row, self.col = None, None

    def __repr__(self):
        return f'{self.name} at ({self.x}, {self.y})'

    def draw(self):
        imageWidth, imageHeight = getImageSize(self.url)
        drawImage(self.url, self.x+2, self.y+2, width=self.drawSize-4, height=self.drawSize-4)

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name and self.x == other.x and self.y == other.y

class Door(Item):
    def __init__(self, name, x, y, size, url=''):
        self.url = url
        super().__init__(name, x, y, size)

    def draw(self):
        imageWidth, imageHeight = getImageSize(self.url)
        drawImage(self.url, self.x, self.y, align='center', width=35, height=35)


class healthItem(Item):
    def __init__(self, name, x, y, size):
        super().__init__(name, x, y, size)
        self.healAmount = 20