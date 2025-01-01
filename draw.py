import math
import random
import os
from random import randint
from cmu_graphics import *
from boundary import *
from ray import *
from particle import *
from player import *
from item import *
from button import *
# 15-112 Term Project by Graham Felton (gtf): "Dungeon Crawler"
#                                                                               _____
#  ____________ ______   _____    _____    _____            _____          _____\    \       ____    _____    _____
#  \           \\     \  \    \  |\    \   \    \      _____\    \_       /    / |    |  ____\_  \__|\    \   \    \
#   \           \\    |  |    |   \\    \   |    |    /     /|     |     /    /  /___/| /     /     \\\    \   |    |
#    |    /\     ||   |  |    |    \\    \  |    |   /     / /____/|    |    |__ |___|//     /\      |\\    \  |    |
#    |   |  |    ||    \_/   /|     \|    \ |    |  |     | |_____|/    |       \     |     |  |     | \|    \ |    |
#    |    \/     ||\         \|      |     \|    |  |     | |_________  |     __/ __  |     |  |     |  |     \|    |
#   /           /|| \         \__   /     /\      \ |\     \|\        \ |\    \  /  \ |     | /     /| /     /\      \
#  /___________/ | \ \_____/\    \ /_____/ /______/|| \_____\|    |\__/|| \____\/    ||\     \_____/ |/_____/ /______/|
# |           | /   \ |    |/___/||      | |     | || |     /____/| | ||| |    |____/|| \_____\   | /|      | |     | |
# |___________|/     \|____|   | ||______|/|_____|/  \|_____|     |\|_|/ \|____|   | | \ |    |___|/ |______|/|_____|/
#                          |___|/                           |____/             |___|/   \|____|     _____
#         _____  ___________          _____           _______     _______  _____               _____\    \ ___________
#    _____\    \_\          \       /      |_        /      /|   |\      \|\    \             /    / |    |\          \
#   /     /|     |\    /\    \     /         \      /      / |   | \      \\\    \           /    /  /___/| \    /\    \
#  /     / /____/| |   \_\    |   |     /\    \    |      /  |___|  \      |\\    \         |    |__ |___|/  |   \_\    |
# |     | |____|/  |      ___/    |    |  |    \   |      |  |   |  |      | \|    | ______ |       \        |      ___/
# |     |  _____   |      \  ____ |     \/      \  |       \ \   / /       |  |    |/      \|     __/ __     |      \  ____
# |\     \|\    \ /     /\ \/    \|\      /\     \ |      |\\/   \//|      |  /            ||\    \  /  \   /     /\ \/    \
# | \_____\|    |/_____/ |\______|| \_____\ \_____\|\_____\|\_____/|/_____/| /_____/\_____/|| \____\/    | /_____/ |\______|
# | |     /____/||     | | |     || |     | |     || |     | |   | |     | ||      | |    ||| |    |____/| |     | | |     |
#  \|_____|    |||_____|/ \|_____| \|_____|\|_____| \|_____|\|___|/|_____|/ |______|/|____|/ \|____|   | | |_____|/ \|_____|
#         |____|/                                                                                  |___|/
# Note: Raycasting logic based off of a haxe3 implementation from Redblob games: https://www.redblobgames.com/articles/visibility/
# ascii art from http://patorjk.com/
def onAppStart(app):
    resetApp(app)

def resetApp(app):
    app.dir = os.getcwd()
    app.stepsPerSecond = 10
    app.height = 800
    app.width = 800
    app.mouseLoc = Point(0, 0)
    app.screens = ['winner', 'dead', 'main_menu', 'combat', 'inventory', 'level1', 'level2', 'level3', 'lastlevel']
    app.stepsPerSecond = 100
    app.paused = False
    app.combat = False
    app.currentGameState = 'main_menu'
    app.lastGameState = None
    app.background = 'black'
    app.mouseX, app.mouseY = 0, 0
    app.showWarning = False
    regenLevel(app)
    #################
    # Make Main Menu
    #################
    app.menu_buttons = [Button('Start Game', app.width/2, app.height/2, 150, 50, '')]
    ###################
    # Combat Screen
    ###################
    app.combat_currentEnemy = None
    app.combat_buttons = [CombatButton('Head', app.width / 2, 150, 200, 200, '', 50),
                          CombatButton('Left', 150, app.height / 2 - 50, 200, 200, '', 85),
                          CombatButton('Right', app.width - 150, app.height / 2 - 50, 200, 200, '', 85),
                          CombatButton('Chest', app.width / 2, app.height / 2, 200, 200, '', 70)]
##################################################################################
# MAIN MENU
##################################################################################
def drawMainMenuButtons(app):
    for button in app.menu_buttons:
        button.draw()

def drawTitle(app):
    drawLabel('DUNGEON CRAW112R', app.width/2, 50, size=25, bold=True, fill='white')

def drawPicFrame(x, y, width, height):
    # once again, another picture from pinterest:
    # https://i.pinimg.com/736x/db/7a/a5/db7aa5b11b436a2451d089fbddb38348.jpg
    drawImage(r'frame.jpg', x, y, width=width, height=height, align='center')

def main_menu_redrawAll(app):
    drawPicFrame(app.width/2, 50, 400, 100)
    drawTitle(app)
    drawPicFrame(app.width/2, app.height/2+1, 200, 100)
    drawMainMenuButtons(app)

def main_menu_onMouseMove(app, mouseX, mouseY):
    app.mouseX, app.mouseY = mouseX, mouseY
    for button in app.menu_buttons:
        if button.isBeingHovered(mouseX, mouseY):
            button.bgColor = 'white'
            button.textColor = 'black'
        else:
            button.bgColor = 'blue'
            button.textColor = 'white'

def main_menu_onMousePress(app, mouseX, mouseY):
    for button in app.menu_buttons:
        if button.isBeingHovered(mouseX, mouseY) and button.name == 'Start Game':
            app.lastGameState = app.currentGameState
            app.currentGameState = 'level1'
            regenInventory(app)
            setActiveScreen('level1')

def regenInventory(app):
    #################
    # Make Inventory
    #################
    rows, cols = 6, 5
    app.margin = 10
    app.cellSize = 50
    app.inventory_item_slots = [[None] * cols for _ in range(rows)]
    app.inventory_equippedItem = Item('Sword', 0, 0, 10, url=r'sword.jpg')
    app.inventory_cells = [[None] * cols for _ in range(rows)]
    app.inventory_selectedItem = None
    app.inventoryLeft = app.width/2 - ((app.margin * cols) + (app.cellSize * cols))/2
    app.inventoryBottom = (app.cellSize + app.margin * rows) + ((app.cellSize + app.margin) * rows)
    buttonWidth = (app.margin + app.cellSize * cols)/2 - app.margin
    app.inventory_buttons = [Button('Use Item', app.width/2, app.inventoryBottom + 50, 200, 50, ''),
                             Button('Exit', app.width-50, 25, 100, 50, '')]
    for row in range(rows):
        for col in range(cols):
            app.inventory_cells[row][col] = Cell(app.inventoryLeft + ((app.cellSize + app.margin) * col),
                                                 (app.cellSize + app.margin * 2) + ((app.cellSize + app.margin) * row),
                                                 app.cellSize, app.cellSize, row, col)
    app.inventory_cells[0][0].item = app.inventory_equippedItem
    app.inventory_equippedItem.drawSize = app.cellSize

##################################################################################
# INVENTORY SCREEN
##################################################################################
def drawInventory(app):
    drawPicFrame(app.width / 2, app.height/2-150, 400, 600)
    drawPicFrame(app.width / 2, app.inventoryBottom + 140, 350, 40)
    playerHPbar = HealthBar('Player Health', app.width/2, app.inventoryBottom + 140, 250, 20, '', app.player.health)
    playerHPbar.draw()
    for button in app.inventory_buttons:
        button.draw()
    drawLabel('INVENTORY', app.width / 2, 25, size=25, bold=True, fill='white')
    drawLabel('YOUR HEALTH:', app.width / 2, app.inventoryBottom+100, size=25, bold=True, fill='white')
    # draw inventory cells
    for row in range(len(app.inventory_cells)):
        for col in range(len(app.inventory_cells[0])):
            currentCell = app.inventory_cells[row][col]
            currentCell.draw()
            currentItem = currentCell.item
            if currentItem: # check for an item in the slot
                # set the position of the item in the inventory screen
                currentItem.x, currentItem.y = app.inventoryLeft + ((app.cellSize + app.margin) * col), (app.cellSize + app.margin * 2) + ((app.cellSize + app.margin) * row)
                currentItem.draw()

def inventory_redrawAll(app):
    drawInventory(app)

def inventory_onMouseMove(app, mouseX, mouseY):
    app.mouseX, app.mouseY = mouseX, mouseY
    for button in app.inventory_buttons:
        if button.isBeingHovered(mouseX, mouseY):
            button.bgColor = 'white'
            button.textColor = 'black'
        else:
            button.bgColor = 'blue'
            button.textColor = 'white'
    # print(app.inventory_cells)
    for row in range(len(app.inventory_cells)):
        for col in range(len(app.inventory_cells[0])):
            currentCell = app.inventory_cells[row][col]
            if currentCell.isBeingHovered(mouseX, mouseY):
                currentCell.color = 'white'
            else:
                currentCell.color = 'black'

def inventory_onMousePress(app, mouseX, mouseY):
    for row in range(len(app.inventory_cells)):
        for col in range(len(app.inventory_cells[0])):
            currentCell = app.inventory_cells[row][col]
            itemInCell = app.inventory_cells[row][col].item
            if currentCell.isBeingHovered(mouseX, mouseY) and itemInCell:
                if app.inventory_selectedItem: # deselect item
                    app.inventory_selectedItem = None
                    currentCell.borderColor = 'white'
                    break
                else:
                    app.inventory_selectedItem = itemInCell
                    currentCell.borderColor = 'red'
    for button in app.inventory_buttons:
        if button.isBeingHovered(mouseX, mouseY):
            if button.name == 'Use Item':
                if app.player.health < 100:
                    useItem(app, app.inventory_selectedItem)
                    currentCell.borderColor = 'white'
                    print(currentCell)
                    inventory_removeItem(app, app.inventory_selectedItem)
                    app.inventory_selectedItem = None
                    print('player health:', app.player.health)
    for button in app.inventory_buttons:
        if button.isBeingHovered(mouseX, mouseY) and button.name == 'Exit':
            app.currentGameState = app.lastGameState
            app.lastGameState = 'inventory'
            setActiveScreen(app.currentGameState)

def inventory_onKeyPress(app, key):
    if key == 'escape':
        app.currentGameState = app.lastGameState
        app.lastGameState = 'inventory'
        setActiveScreen(app.currentGameState)
##################################################################################
# COMBAT STATE
##################################################################################
def drawCombatMenu(app):
    imgWidth, imgHeight = getImageSize(app.combat_currentEnemy.url)
    drawImage(app.combat_currentEnemy.url, app.width/2, app.height/2,
              width=imgWidth, height=imgHeight, align='center')
    player_hpBar = HealthBar('Your Health', app.width/2, app.height - 20,
                             200, 20, '', app.player.health)
    player_hpBar.draw()
    enemy_hpBar = HealthBar(app.combat_currentEnemy.name,
                               app.width/2,
                               50,
                               100, 10, '',
                               app.combat_currentEnemy.health) if app.combat_currentEnemy else None
    drawLabel(f'Enemy: {app.combat_currentEnemy.name}', app.width/2, 25,
              size=25, bold=True, fill='white')
    drawLabel(f'Your Health:', app.width/2, app.height - 40, size=15, fill='white')
    for hitbox in app.combat_currentEnemy.anatomy:
        currentHitboxHP = app.combat_currentEnemy.anatomy[hitbox][0]
        for button in app.combat_buttons:
            if button.isBeingHovered(app.mouseX, app.mouseY):
                drawLabel(f'{button.chance}% chance to hit {button.name}',
                          app.mouseX + 40, app.mouseY, fill=rgb(0,255,0), align='left')
            # check for dead hitboxes, then draw them as grey
            if button.name == hitbox:
                if 0.0 <= currentHitboxHP <= 0.01:
                    button.bgColor = 'grey'
                button.draw()

    enemy_hpBar.draw()
    currentPlayerDmg = app.playerMoves[-1] if app.playerMoves else 0
    currentEnemyDmg = app.enemyMoves[-1] if app.enemyMoves else 0
    drawLabel(f'You dealt: {currentPlayerDmg} damage', app.width-50, 50,
              size=20, bold=True, fill='white', align='right')
    drawLabel(f'Enemy dealt: {currentEnemyDmg} damage', app.width-50, app.height-50,
              size=20, bold=True, fill='red', align='right')

def combat_redrawAll(app):
    drawCombatMenu(app)

def combat_onMouseMove(app, mouseX, mouseY):
    app.mouseX, app.mouseY = mouseX, mouseY
    for button in app.combat_buttons:
        if button.isBeingHovered(mouseX, mouseY):
            app.currentButton = button
            button.bgColor = 'white'
            button.textColor = 'black'
        else:
            button.bgColor = 'blue'
            button.textColor = 'white'

def tryHit(button):
    # translate chance to float value
    chance = button.chance / 100
    # produce a random float between 0 and 1.0
    hit = random()
    print(f'chance is {chance}, hit is {hit}')
    if hit <= chance:
        return True
    else:
        return False

def enemyAttack(app):
    chance = .35

    hit = random()
    if hit <= chance:
        app.enemyMoves.append(10)
        app.player.health -= 10
    else:
        app.enemyMoves.append(0)


def combat_onMousePress(app, mouseX, mouseY):
    for button in app.combat_buttons:
        # check if the enemy is dead
        if button.isBeingHovered(mouseX, mouseY):
            currentHitbox = button.name
            # attack
            if app.combat_currentEnemy.health > 0:
                if currentHitbox == 'Head':
                    hit = tryHit(button)
                    if hit:
                        app.playerMoves.append(30)
                        app.combat_currentEnemy.health -= 30
                    else:
                        app.playerMoves.append(0)
                elif currentHitbox == 'Chest':
                    hit = tryHit(button)
                    if hit:
                        app.playerMoves.append(20)
                        app.combat_currentEnemy.health -= 20
                    else:
                        app.playerMoves.append(0)
                elif currentHitbox == 'Left':
                    hit = tryHit(button)
                    if hit:
                        app.playerMoves.append(10)
                        app.combat_currentEnemy.health -= 10
                    else:
                        app.playerMoves.append(0)
                elif currentHitbox == 'Right':
                    hit = tryHit(button)
                    if hit:
                        app.playerMoves.append(10)
                        app.combat_currentEnemy.health -= 10
                    else:
                        app.playerMoves.append(0)
                print(app.playerMoves)
    # enemy's turn
    enemyAttack(app)
    # check if we've killed the current enemy
    if (app.combat_currentEnemy.health <= 0):
        setActiveScreen(app.lastGameState) # go back to the current level screen
        app.enemyMoves, app.playerMoves = [], []
        print(app.combat_currentEnemy, app.enemies)
        enemyIndex = app.enemies.index(app.combat_currentEnemy)
        app.enemies.pop(enemyIndex) # remove the enemy from the world
        app.playerParticle.enemies.pop(enemyIndex)
        app.combat = False
        app.currentGameState = app.lastGameState # reset the game states
        app.lastGameState = 'combat'
    if app.player.health <= 0:
        app.combat = False
        print('you died')
        app.lastGameState = app.currentGameState
        app.currentGameState = 'dead'
        setActiveScreen(app.currentGameState)
##################################################################################
# LEVEL 1
##################################################################################
def level1_redrawAll(app):
    level_initDraw(app)

def drawPauseMenu(app):
    drawRect(0, 0, app.width, app.height, fill='white', opacity=70)
    drawLabel('Paused', app.width/2, app.height/2-150, size=20, bold=True)

def level1_onKeyHold(app, keys):
    _onKeyHold(app, keys)

def level1_onKeyPress(app, key):
    _onKeyPress(app, key)

##################################################################################
# LEVEL 2
##################################################################################
def level2_redrawAll(app):
    level_initDraw(app)

def level2_onKeyHold(app, keys):
    _onKeyHold(app, keys)

def level2_onKeyPress(app, key):
    _onKeyPress(app, key)
##################################################################################
# LEVEL 3
##################################################################################
def level3_redrawAll(app):
    level_initDraw(app)

def level3_onKeyHold(app, keys):
    _onKeyHold(app, keys)

def level3_onKeyPress(app, key):
    _onKeyPress(app, key)
##################################################################################
# LAST LEVEL
##################################################################################
def lastlevel_redrawAll(app):
    level_initDraw(app)

def lastlevel_onKeyHold(app, keys):
    _onKeyHold(app, keys)

def lastlevel_onKeyPress(app, key):
    _onKeyPress(app, key)
##################################################################################
# DEAD
##################################################################################
def dead_redrawAll(app):
    drawLabel('YOU DIED', app.width/2, app.height/2-100, size=40, bold=True, fill='red')
    drawLabel("Press 'r' to go back to the main menu",
              app.width/2, app.height/2-50, size=10, bold=True, fill='white')

def dead_onKeyPress(app, key):
    if key == 'r':
        app.currentGameState = 'main_menu'
        app.lastGameState = 'dead'
        regenLevel(app)
        regenInventory(app)
        setActiveScreen(app.currentGameState)
##################################################################################
# WINNER
##################################################################################
def winner_redrawAll(app):
    drawLabel('YOU WIN', app.width/2, app.height/2-100,
              size=40, bold=True, fill='green')
    drawLabel('You successfully survived all levels!', app.width/2, app.height/2-75,
              size=20, bold=True, fill='green')
    drawLabel("Press 'r' to go back to the main menu", app.width/2, app.height/2-50,
              size=10, bold=True, fill='white')

def winner_onKeyPress(app, key):
    if key == 'r':
        app.currentGameState = 'main_menu'
        app.lastGameState = 'dead'
        regenLevel(app)
        regenInventory(app)
        setActiveScreen(app.currentGameState)
##################################################################################
# UBIQUITOUS METHODS
##################################################################################
def isvisible(player, other, bounds):
    # player and other must be points
    ray = Ray(other.x, other.y, player.angleto(other))
    closestPt = other
    closestDist = player.dist(other)
    # cast a ray from the other point in the direction of this point
    # if there is a new point between this point and the other point, it's not visible
    for bound in bounds:
        pt = ray.cast(bound)
        if pt:
            intPt = Point(pt[0], pt[1])
            # if the intersection point is the same point as the one we're checking, ignore it
            if math.isclose(player.x, intPt.x) and math.isclose(player.y, intPt.y):
                continue
            if other.dist(intPt) < closestDist:
                closestPt = intPt
                closestDist = other.dist(intPt)
    if closestDist < player.dist(other):
        return False
    return True

def drawBounds(app):
    for wall in app.walls:
        drawLine(wall.x1, wall.y1, wall.x2, wall.y2, fill='white', lineWidth=1)

def drawRays(app):
    drawRect(0, 0, app.width, app.height/2, fill='white', opacity=10)
    drawRect(0, app.height/2, app.width, app.height/2, fill='white', opacity=20)
    player = Point(app.player.x, app.player.y)
    pDir = Ray(player.x, player.y,
               math.radians(app.playerParticle.direction + app.playerParticle.fov/2))
    visPoints = app.playerParticle.cast(app.walls)
    distances = []
    # check for items/players
    for distance in visPoints:
        key = distance
        current = visPoints[key]
        if type(current) == Point:
            distances.append(distance)
        else: # if we find an entity
            distances.append((distance, current))

    distanceValues = [key for key in visPoints.keys()]
    width = app.width/len(distances) if len(distances) > 0 else app.width
    # logic for drawing walls as columns (height = dist) from: https://lodev.org/cgtutor/raycasting.html
    # draw the walls
    if len(distanceValues) > 0:
        maxDist = (app.width**2 + app.height**2)**0.5
        low = 1/max(distanceValues) if max(distanceValues) != 0 else 0
        high = 1/min(distanceValues) if min(distanceValues) != 0 else 0
        for i in range(len(distances)):
            current = distances[i]
            color = abs(remap(distanceValues[i]**2, 0, maxDist**2, 255, 0))
            x = i * width
            y = app.height/2
            fill = rgb(color, color-50, color) if color >=50 else rgb(0, 0, 0)
            # draw different colored walls depending on the level
            if app.currentGameState == 'level1':
                fill = rgb(color, max(color-50, 0), color)
            elif app.currentGameState == 'level2':
                fill = rgb(color, color, max(color-50, 0))
            elif app.currentGameState == 'level3':
                fill = rgb(max(color-50, 0), color, color)
            elif app.currentGameState == 'lastlevel':
                fill = rgb(max(color-50, 0), max(color-50, 0), color)
            if type(current) != tuple:
                distance = distanceValues[i] if not math.isclose(distanceValues[i], 0) else .01
                height = (1/distance) * (app.height * 20)
                drawRect(x, y, width, height, fill=fill, align='center')
        # draw items, enemies in front of walls
        for i in range(len(distances)):
            current = distances[i]
            color = abs(remap(distanceValues[i]**2, 0, app.height**2, 255, 0))
            x = i * width
            y = app.height/2
            if type(current) == tuple:
                distance = distanceValues[i] if not math.isclose(distanceValues[i], 0) else .01
                entity = current[1]
                print(f'we are drawing {entity}')
                entity.size = (1/distance) * (app.height)
                imgHeight, imgWidth = getImageSize(entity.url)
                imgHeight *= (1/distance) * (app.height/100)
                imgWidth *= (1/distance) * (app.height/100)
                # draw items
                if (entity.name != 'Next Level Door' and
                    type(entity) == Item):
                    drawImage(entity.url, x, y,
                              width=imgWidth, height=imgHeight, align='center')
                # draw enemies
                elif (entity.name != 'Next Level Door'):
                    drawImage(entity.url, x, y,
                              width=imgWidth, height=imgHeight, align='center')
                # draw next level portal
                else:
                    drawImage(entity.url, x, y,
                              width=imgWidth, height=imgHeight, align='center')

# remapping from: https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def remap(value, low1, high1, low2, high2):
    return ((value - low1) / (high1 - low1)) * (high2 - low2) + low2

def sortPoints(app, points):
    seen = set()
    result = []
    player = Point(app.player.x, app.player.y)
    for angle, currentPoint in points:
        if currentPoint in seen:
            continue
        seen.add(currentPoint)
        # normalize the angle to range(0, 2*pi)
        adjustedAng = angle if angle >= 0 else angle + 2 * math.pi
        result.append((adjustedAng, currentPoint))
    sortedPoints = sorted(points, key=lambda point: point[0])
    result = [point[1] for point in sortedPoints]
    print('sorted points:', result)
    return result

def level_initDraw(app):
    drawRays(app)
    if app.showWarning:
        drawLabel('You need to find the key to unlock this door',
                  app.width/2, 20, size=10, fill='red')
    if app.paused:
        drawPauseMenu(app)
    drawLabel(f'{app.currentGameState}', app.width/2, 10,
              size=10, fill='white')

def getNextOpenSlot(inventory):
    rows, cols = len(inventory), len(inventory[0])
    for row in range(rows):
        for col in range(cols):
            if inventory[row][col].item == None:
                return row, col
    return None

def _onKeyHold(app, keys):
    if not app.paused:
        enemiesSeekPlayer(app)
        app.playerParticle.recalc()
        app.closestWall = app.player.getClosestWall(app.walls)
        ###################
        # PLAYER COLLISIONS
        ###################
        for item in app.items:
            currentItem = app.items[item]
            # pickup items
            if app.player.isColliding(currentItem) and currentItem != app.nextLevelDoor:
                targetSlot = getNextOpenSlot(app.inventory_cells)
                # if there exists a free space in the inventory, pick up the item
                if targetSlot:
                    trow, tcol = targetSlot
                    currentItem.row, currentItem.col = trow, tcol
                    app.inventory_cells[trow][tcol].item = currentItem
                    app.player.pickupItem(currentItem)
                    currentItem.drawSize = app.cellSize
                    print(app.inventory_cells)
                # remove the item from the world and the player particle inventory
                app.items.pop(item)
                itemIndex = app.playerParticle.items.index(currentItem)
                app.playerParticle.items.pop(itemIndex)
                break
            # edge case for the last level - end the game
            if (app.player.isColliding(app.nextLevelDoor) and
                itemInInventory(app, app.nextLevelKey) and
                app.currentGameState == 'lastlevel'):
                app.lastGameState = app.currentGameState
                app.currentGameState = 'winner'
                regenInventory(app)
                setActiveScreen('winner')
            # if we have the key and we've found the door, generate a new level
            elif (app.player.isColliding(app.nextLevelDoor) and
                itemInInventory(app, app.nextLevelKey) and
                app.currentGameState != 'lastlevel'):
                print('current state', app.currentGameState)
                inventory_removeItem(app, app.nextLevelKey)
                app.items[app.nextLevelKey.name] = app.nextLevelKey
                app.lastGameState = app.currentGameState
                app.currentGameState = app.screens[app.screens.index(app.currentGameState) + 1]
                setActiveScreen(app.currentGameState)
                regenLevel(app)
                return
            # tell player to find key if they are trying to enter the door without it
            elif (app.player.isColliding(app.nextLevelDoor) and
                  not itemInInventory(app, app.nextLevelKey)):
                app.showWarning = True
            else:
                app.showWarning = False

        # only allow movement if the game is not paused and we're not in combat
        if not app.paused and not app.combat:
            # pass
            for enemy in app.enemies:
                if app.player.isVisible(enemy, app.interiorWalls):
                    # enemy.seek(app.player)
                    pass
                if app.player.isColliding(enemy):  # enter the combat game state
                    app.combat = True
                    app.combat_currentEnemy = enemy
                    app.lastGameState = app.currentGameState
                    app.currentGameState = 'combat'
                    setActiveScreen('combat')
        #################
        # PLAYER MOVEMENT
        #################
        # this math is from https://stackoverflow.com/questions/50088773/formula-math-calculations-for-moving-a-player-forward-based-on-direction-facin
        theta = math.radians(app.player.direction)
        dir = theta if theta >= 0 else 2 * math.pi + theta
        moveDist = app.height * 0.005
        if 'w' in keys:
            print(theta)
            app.player.y -= moveDist * math.sin(theta)
            app.player.x -= moveDist * math.cos(theta)
            app.playerParticle.y = app.player.y
            app.playerParticle.x = app.player.x
        if 'a' in keys:
            app.player.y -= moveDist * math.sin(theta - (math.pi/2))
            app.player.x -= moveDist * math.cos(theta - (math.pi/2))
            app.playerParticle.y = app.player.y
            app.playerParticle.x = app.player.x
        if 'd' in keys:
            app.player.y -= moveDist * math.sin(theta + (math.pi/2))
            app.player.x -= moveDist * math.cos(theta + (math.pi/2))
            app.playerParticle.y = app.player.y
            app.playerParticle.x = app.player.x
        if 's' in keys:
            app.player.y += moveDist * math.sin(theta)
            app.player.x += moveDist * math.cos(theta)
            app.playerParticle.y = app.player.y
            app.playerParticle.x = app.player.x
        # rotate the camera
        if 'left' in keys:
            app.playerParticle.direction -= 2
            app.playerParticle.normalizeDir()
            app.player.direction = app.playerParticle.direction
        if 'right' in keys:
            app.playerParticle.direction += 2
            app.playerParticle.normalizeDir()
            app.player.direction = app.playerParticle.direction
        app.player.checkBounds(app.width, app.height)

def _onKeyPress(app, key):
    if key == 'escape' and 'level' in app.currentGameState:
        app.paused = not app.paused
    if key == 'i' and 'level' in app.currentGameState:
        app.lastGameState = app.currentGameState
        app.currentGameState = 'inventory'
        setActiveScreen('inventory')

def getNamesFromFile(filename):
    file = open(filename, 'r')
    return [line.strip() for line in file.readlines()]

def useItem(app, item):
    # healing items
    if 'potion' in item.url:
        app.player.health += 20

def itemInInventory(app, val):
    rows, cols = len(app.inventory_cells), len(app.inventory_cells[0])
    for row in range(rows):
        for col in range(cols):
            if val == app.inventory_cells[row][col].item:
                return True
    return False

def inventory_removeItem(app, item):
    rows, cols = len(app.inventory_cells), len(app.inventory_cells[0])
    for row in range(rows):
        for col in range(cols):
            if item == app.inventory_cells[row][col].item:
                app.inventory_cells[row][col].item = None
    return False

def enemiesSeekPlayer(app):
    moveDist = 2
    for enemy in app.enemies:
        a = math.atan2(app.player.y - enemy.y, app.player.x - enemy.x)
        angleToPlayer = a if a >= 0 else a + 2 * math.pi
        enemy.y -= moveDist * -math.sin(angleToPlayer)
        enemy.x -= moveDist * -math.cos(angleToPlayer)

def regenLevel(app):
    #################
    # Reset Player
    #################
    app.player = Player(200, 375)
    app.playerParticle = Particle(app.player.x, app.player.y)
    #################
    # Make Items
    #################
    app.nextLevelKey = Item('Key to next level',
                            randrange(20, app.width - 20),
                            randrange(20, app.height - 20), 40,
                            url=r"key.jpg")
    app.testItem = Item('Test Item1',
                        randrange(20, app.width - 20),
                        randrange(20, app.height - 20), 40, 'red',
                        url=r"potion.jpg")
    app.nextLevelDoor = Item('Next Level Door',
                        randrange(20, app.width - 20),
                        randrange(20, app.height - 20), 40,
                        url=r"door2.jpg")
    app.items = {app.testItem.name: app.testItem,
                 app.nextLevelKey.name: app.nextLevelKey,
                 app.nextLevelDoor.name: app.nextLevelDoor}
    #################
    # Make Walls
    #################
    top = Boundary(0, 0, app.width, 0)
    right = Boundary(app.width, 0, app.width, app.height)
    bottom = Boundary(0, app.height, app.width, app.height)
    left = Boundary(0, 0, 0, app.height)
    app.walls = [top, right, bottom, left]
    app.extWalls = [top, right, bottom, left]
    app.interiorWalls = []
    # add random boundaries
    for i in range(4):
        app.interiorWalls.append(Boundary(randrange(0, app.width),
                                          randrange(0, app.height),
                                          randrange(0, app.width),
                                          randrange(0, app.height))
                                )
    app.walls.extend(app.interiorWalls)
    #################
    # Make Enemies
    #################
    # images are from pinterest
    # sword - https://www.pinterest.com/pin/31736372370447515/
    # key - https://www.pinterest.com/pin/31736372370447418/
    # door - https://www.pinterest.com/pin/31736372370447413/
    # potion - https://www.pinterest.com/pin/31736372370447409/
    # knight - https://www.pinterest.com/pin/31736372370444982/
    enemy1 = Enemy(randrange(20, app.width - 20),
                   randrange(20, app.height - 20),
                   'Knight', r"knight.jpg")
    enemy2 = Enemy(randrange(20, app.width - 20),
                   randrange(20, app.height - 20),
                   'Knight', r"knight.jpg")
    app.enemies = [enemy1, enemy2]
    app.playerParticle.enemies.extend(app.enemies)
    app.playerParticle.items.extend([app.items[key] for key in app.items])
    app.playerMoves = []
    app.enemyMoves = []

def main():
    runAppWithScreens(initialScreen='main_menu')

main()