#!/usr/bin/env python3
import pygame # library to generate the graphic interface
import numpy as np # library to handle matrices
import time # to set a delay between each iteration


# -------------     FUNCTIONS      -------------

def constant(f): #define of a constant class
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class color():
    def __init__(self):
        self.BG = (25, 25, 25)
        self.GRID = (128, 128, 128)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DBLUE = (0, 153, 255) # L'
        self.LBLUE = (102, 255, 255) # Straight
        self.PURPLE = (153, 51, 255) # T
        self.GREEN = (102, 255, 102) #skew
        self.YELLOW = (255, 255, 102) #square
        self.ORANGE = (255, 102, 0) # L
        self.RED = (255, 80, 80) # Skew'
    def RANDOM(self):
        colorSet = dict(self.__dict__)
        for x in ["BG", "GRID", "WHITE", "BLACK"]: del colorSet[x] # Remove not wanted colors
        list = [colorSet[colorTitle] for colorTitle in [colorTitle for colorTitle in colorSet]]
        return list[np.random.randint(len(list))]

def getCubeCoord(x, y, *smaller): # Returns the same coordinates with the margin frame
    smallerC = 0 if not smaller else round(sizeWidthX / 14)
    rawCoord = [ # get coord of the cornes of the square
        (x * sizeWidthX + smallerC, y * sizeWidthY + smallerC),
        ((x + 1) * sizeWidthX - smallerC, y * sizeWidthY + smallerC),
        ((x + 1) * sizeWidthX - smallerC, (y + 1) * sizeWidthY - smallerC),
        (x * sizeWidthX + smallerC, (y + 1) * sizeWidthY - smallerC)
    ]
    return [tuple(map(lambda i: i + marginFrame, tu)) for tu in rawCoord]

def updateScreen():
    screen.fill(COLOR.BG) # Clean screen
    for x in range(sizeX): # for each spot in the grid
        for y in range(sizeY):
            # Draw the grid
            pygame.draw.polygon(screen, COLOR.GRID, getCubeCoord(x, y), 1) # print the grid
            if(grid[x, y] != None): # if block there
                pygame.draw.polygon(screen, grid[x, y], getCubeCoord(x, y, True), 0) # print it
    # print preview grid
    for x in range(4):
        for y in range(2):
            pygame.draw.polygon(screen, COLOR.GRID, getCubeCoord(x + 16, y + 1), 1)
    
    #print current piece
    for b in currentPiece.pieces:
        pygame.draw.polygon(screen, b.color, getCubeCoord(b.x, b.y, True), 0)
    
    # print nextPiece
    for b in nextPiece.pieces:
        pygame.draw.polygon(screen, b.color, getCubeCoord(b.x + 16, b.y + 1, True), 0)

    # Score and level:
    screen.blit(scoreLabel, (17.25 * sizeWidthX, 5 * sizeWidthY))
    screen.blit(font.render(str(score), False, COLOR.WHITE), ((18.5 - (len(str(score))-1)/4) * sizeWidthX, 6 * sizeWidthY))
    screen.blit(levelLabel, (17.25 * sizeWidthX, 9 * sizeWidthY))
    screen.blit(font.render(str(level), False, COLOR.WHITE), ((18.5 - (len(str(level))-1)/4) * sizeWidthX, 10 * sizeWidthY))
    pygame.display.flip() # Update the screen


# -------------     CLASSES      -------------

class tetrisPiece:
    def __init__(self):
        # self.color = COLOR.RANDOM() # Get color
        self.pieces = [] # Here the pieces will be stored
        # Straight: |   Square:   |   T:        |   L:        |   L':       |   Skew:     |   Skew':
        # 0 0 0 0   |   - 0 0 -   |   - 0 - -   |   - - 0 -   |   0 - - -   |   - 0 0 -   |   0 0 - -
        # - - - -   |   - 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 - -   |   - 0 0 -
        self.type = np.random.randint(7) 
        # print(self.getTypeName() + " piece created")
        if self.type == 0: # "Straight"
            self.color = COLOR.LBLUE
            self.pieces = [block(i, 0, self.color)for i in range(4)]
        elif self.type == 1: # "Square"
            self.color = COLOR.YELLOW
            self.pieces = [block(i + 1, j, self.color)for i in range(2) for j in range(2)]
        elif self.type == 2: # "T"
            self.color = COLOR.PURPLE
            self.pieces = [block(i, 1, self.color) for i in range(3)] + [block(1, 0, self.color)]
        elif self.type == 3: # "L"
            self.color = COLOR.ORANGE
            self.pieces = [block(i, 1, self.color) for i in range(3)] + [block(2, 0, self.color)]
        elif self.type == 4: # "L'"
            self.color = COLOR.DBLUE
            self.pieces = [block(i, 1, self.color) for i in range(3)] + [block(0, 0, self.color)]
        elif self.type == 5: # "Skew"
            self.color = COLOR.GREEN
            self.pieces = [block(i, 1, self.color) for i in range(2)] + [block(i + 1, 0, self.color)for i in range(2)]
        elif self.type == 6: # "Skew'"
            self.color = COLOR.RED
            self.pieces = [block(i, 0, self.color) for i in range(2)] + [block(i + 1, 1, self.color)for i in range(2)]

    def start(self):
        self.move(5, 0)

    def validMove(self, x, y): # Check if all moved pieces in valid place
        for b in self.pieces:
            if not b.validBlock(x, y): # If not valid place
               return False
        return True

    def move(self, x, y):
        if not self.validMove(x, y):
            return # If not valid move, do not do it
        for b in self.pieces:
            b.x = b.x + x
            b.y = b.y + y

    def canFall(self):
        for b in self.pieces:
            if not b.validBlock(0, 1) or grid[b.x, b.y + 1] != None: # If someone below:
                return False
        return True 

    def fall(self):
        if self.canFall():
            for b in self.pieces:
                b.y = b.y + 1

    def validRotation(self, blocks):
        for b in blocks:
            if not b.validBlock():
                return False
        return True

    def rotate(self):
        if self.type == 1: # square
            return
        pieces = [b.copy() for b in self.pieces]
        dh = 1 if pieces[0].y == pieces[1].y else 0 # Horizontal position (dv = ((dh + 1) % 2))
        ini = [pieces[2].x, pieces[2].y]
        if self.type == 0: # "Straight"
            for i in range(-2, 2, 1):
                pieces[i + 2].x = ini[0] + i * ((dh + 1) % 2)
                pieces[i + 2].y = ini[1] + i * dh
        elif self.type == 5: # "Skew":
            for i in range(2):
                pieces[i].x = ini[0] - 1 + i * ((dh + 1) % 2)
                pieces[i].y = ini[1] + (- 1 + i) * dh + ((dh + 1) % 2)
            pieces[3].x = ini[0] + ((dh + 1) % 2)
            pieces[3].y = ini[1] + dh
        elif self.type == 6: # "Skew'":
            for i in range(2):
                pieces[i].x = ini[0] + dh + (-1 + i) * ((dh + 1) % 2)
                pieces[i].y = ini[1] - 1 + i * dh 
            pieces[3].x = ini[0] + ((dh + 1) % 2)
            pieces[3].y = ini[1] + dh
        else: # T, L, L'
            ini = [pieces[1].x, pieces[1].y]
            if self.type == 2: # "T"
                dh = 1 if pieces[0].x < pieces[1].x or pieces[0].y < pieces[1].y else 0
                dz = 1 if pieces[0].y == pieces[1].y else 0 # Horizontal position
                for i in range(-1, 2, 1):
                    pieces[i + 1].x = ini[0] + i * (dh - ((dh + 1) % 2)) * ((dz + 1) % 2)
                    pieces[i + 1].y = ini[1] + i * (- dh + ((dh + 1) % 2)) * dz
                pieces[3].x = ini[0] + (dh - ((dh + 1) % 2)) * dz
                pieces[3].y = ini[1] + (- dh + ((dh + 1) % 2)) * ((dz + 1) % 2)
            else:
                dt = 1 if self.type == 3 else -1 # 1 if L, -1 if L'
                dh = 1 if pieces[0].y == pieces[1].y else 0 # Horizontal position (vertical = ((dh + 1) % 2))
                dz = 1 if pieces[0].x < pieces[1].x or pieces[0].y < pieces[1].y else -1 # 1 or 2
                for i in range(-1, 2, 1):
                    pieces[i + 1].x = ini[0] - ((dh + 1) % 2) * dz * i
                    pieces[i + 1].y = ini[1] + dh * dz * i
                pieces[3].x = ini[0] + dh * dz - ((dh + 1) % 2) * dz * dt
                pieces[3].y = ini[1] + dh * dz * dt + ((dh + 1) % 2) * dz

        # At this point, pieces are rotated
        if(self.validRotation(pieces)):
            self.pieces = [b for b in pieces]

    def typeConv(self): # to convert a int to the equivalent piece
        return ["Straight", "Square", "T", "L", "L'", "Skew", "Skew'"]
    
    def getTypeName(self):
        return self.typeConv()[int(self.type)]
    
    def copy(self):
        newPiece = tetrisPiece()
        newPiece.type = self.type
        newPiece = [b.copy() for b in self.pieces]
        return newPiece

    def getPosition(self):
        minX, minY, maxX, maxY = sizeX, sizeY, 0, 0
        for b in self.pieces:
            if b.x < minX: 
                minX = b.x
            elif b.x > maxX:
                maxX = b.x
            if b.y < minY: 
                minY = b.y
            elif b.y > maxY:
                maxY = b.y
        return [[minX, minY], [maxX, maxY]]

class block:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c

    def copy(self):
        return block(self.x, self.y, self.color)

    def validBlock(self, x = 0, y = 0):
        return self.x + x >= 0 and self.x + x < sizeX and self.y + y >= 0 and self.y + y < sizeY and grid[self.x + x, self.y + y] == None


# -------------     CODE      -------------

pygame.init() # Init pygame
pygame.display.set_caption("Jkutkut's Tetris") # Set the title of the game

# CONSTANTS:
width = 500 
sizeX, sizeY = 14, 20 # Number of cell spots in each axis (horizontal, vertical)
height = int(sizeY * width / sizeX)
extraWidth = 300 # Some space to display the score, level, next piece...
marginFrame = 20
sizeWidthX = width / sizeX # Size of each spot
sizeWidthY = height / sizeY
COLOR = color() # Get the color class with the constants
font = pygame.font.Font('freesansbold.ttf', 32) 
scoreLabel = font.render('Score:', False, COLOR.WHITE) 
levelLabel = font.render('Level:', False, COLOR.WHITE) 


# Variables:
score, level = 0, 0
currentPiece, nextPiece = None, None
grid = np.matrix([[None for j in range(sizeY)] for i in range(sizeX)])# Init grid: None = empty, else = filled
currentPiece = tetrisPiece() # Piece that is going to start falling
nextPiece = tetrisPiece() # Next piece
currentPiece.start() # Place the currentPiece on the 
screen = pygame.display.set_mode((width + extraWidth + 2 * marginFrame, height + 2 * marginFrame)) # Set the size of the window
lastGameTick = time.process_time() # store when we started (updates the screen)
lastKeyTick = time.process_time() # (updates the keys pressed to enable hold controls)
gameRunning = True # If false, the game stops
running = True
pause = False

keys = {"up": 0, "down": 0, "right": 0, "left": 0} # 0 = key up, > 0 => Key down


# timeRunning = False # If true, time runs (so iterations occur)
while running:
    while gameRunning:
        # Check rows to add score and remove rows
        validRows = 0
        for y in range(sizeY):
            valid = True
            for x in range(sizeX):
                if grid[x, y] == None:
                    valid = False
                    break
            if valid: # If row filled
                validRows = validRows + 1
                for x in range(sizeX):
                    grid[x, y] = None
                for y2 in range(y, 0, -1): # Make all rows fall. Last row always empty
                    for x in range(sizeX):
                        grid[x, y2] = grid[x, y2 - 1]
        if validRows > 0:
            score = score + validRows * 100 + (validRows - 1) * 100 # Update score
            level = int(score / 1000)

        if not pause and time.process_time() - lastGameTick > 0.25 - level/100: # Update the screen but game ticks every some period 
            lastGameTick = time.process_time() # Update current game tick
            if(currentPiece.canFall()):
                currentPiece.fall()
            else:
                for b in currentPiece.pieces:
                    grid[b.x, b.y] = b.color
                currentPiece = nextPiece
                nextPiece = tetrisPiece()
                currentPiece.start()
                if(currentPiece.getPosition()[0][0] < 2):
                    print("Press R or space to restart")
                    for x in range(sizeX):
                        for y in range(sizeY):
                            grid[x, y] = COLOR.RANDOM()
                    gameRunning = False

        if not pause and time.process_time() - lastKeyTick > 0.025: # key control
            lastKeyTick = time.process_time()
            k = pygame.key.get_pressed()  #checking pressed keys
            if k[pygame.K_DOWN] or k[pygame.K_s]: # arrow down
                keys["down"] = keys["down"] + 1
                if keys["down"] > 3:
                    currentPiece.fall()
            else:
                keys["down"] = 0
            if k[pygame.K_RIGHT] or k[pygame.K_d]: # arrow right
                keys["right"] = keys["right"] + 1
                if keys["right"] > 3:
                    currentPiece.move(1, 0)
            else:
                keys["right"] = 0
            if k[pygame.K_LEFT] or k[pygame.K_a]: # arrow left
                keys["left"] = keys["left"] + 1
                if keys["left"] > 3:
                    currentPiece.move(-1, 0)
            else:
                keys["left"] = 0

        for event in pygame.event.get(): # for each event
            if event.type == pygame.QUIT: # if quit btn pressed
                gameRunning = False # no longer running game
                running = False

            elif (event.type == pygame.ACTIVEEVENT and event.state == 2): # If change on the focus of the window
                if event.gain == 0: # If focus lost
                    print("lost focus")
                    pause = True
                elif event.gain == 1: # If focus recovered
                    print("focus")
                    pause = False
                    lastKeyTick = time.process_time()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Space pressed
                    while currentPiece.canFall(): currentPiece.fall()
                elif event.key == pygame.K_UP or event.key == pygame.K_w: # Arrow up
                    currentPiece.rotate()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: # Arrow down
                    currentPiece.fall()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Arrow right
                    currentPiece.move(1, 0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: # Arrow left
                    currentPiece.move(-1, 0)
                #print(event.key, pygame.K_UP)
        updateScreen()


    # Game not Running at this point
    for event in pygame.event.get(): # for each event
        if event.type == pygame.QUIT: # if quit btn pressed
            running = False # no longer running
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == 114 or event.key == 32: # R or space pressed: restart game
                gameRunning = True
                score = 0
                level = 0
                grid = np.matrix([[None for j in range(sizeY)] for i in range(sizeX)])
                currentPiece = tetrisPiece()
                nextPiece = tetrisPiece()
                currentPiece.start()

print("Thanks for playing, I hope you liked it.")
print("See more projects like this one on https://github.com/jkutkut/")
pygame.quit() # End the pygame
