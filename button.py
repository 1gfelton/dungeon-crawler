from cmu_graphics import *

class Button:
    def __init__(self, name, x, y, width, height, imagePath, chance=0):
        self.name = name
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.image = imagePath
        self.bgColor = 'blue'
        self.textColor = 'white'
        self.chance = chance

    def isBeingHovered(self, x, y):
        if (self.x - self.width/2 <= x <= self.x + self.width/2 and
            self.y - self.height/2 <= y <= self.y + self.height/2):
            return True
        return False

    def __repr__(self):
        return f'Button {self.name}'

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, align='center', fill=self.bgColor)
        drawLabel(f'{self.name}', self.x, self.y, fill=self.textColor)

class HealthBar(Button):
    def __init__(self, name, x, y, width, height, imagePath, hitboxHealth, chance=0):
        super().__init__(name, x, y, width, height, imagePath)
        self.hitboxHealth = hitboxHealth
        self.color = 'red' if 0.0 <= hitboxHealth <= 0.01 else 'grey'
        self.chance = chance

    def __repr__(self):
        return f'HealthBar {self.name}, {self.hitboxHealth} hp'

    def draw(self):
        width = self.width * self.hitboxHealth/100 + .1 if self.width * self.hitboxHealth/100 > 0 else .1
        drawRect(self.x - self.width/2, self.y - self.height/2, self.width * self.hitboxHealth/100 + .1, self.height, fill='red')
        drawLabel(f'HP: {int(self.hitboxHealth)}', self.x, self.y, fill=self.textColor)

class Cell:
    def __init__(self, x, y, width, height, row, col):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.row, self.col = row, col
        self.leftBound = self.x
        self.rightBound = self.x + width
        self.topBound = self.y
        self.bottomBound = self.y + height
        self.color = 'black'
        self.borderColor = 'white'
        self.item = None

    def __repr__(self):
        return f'Inventory Cell at row: {self.row}, col: {self.col}'

    def isBeingHovered(self, x, y):
        if (self.leftBound <= x <= self.rightBound and
            self.topBound <= y <= self.bottomBound):
            return True
        return False

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill=self.color, border=self.borderColor)

class CombatButton(Button):
    def __init__(self, name, x, y, width, height, imagePath, chance=0):
        super().__init__(name, x, y, width, height, imagePath, chance)

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill=None, border='red', align='center')
