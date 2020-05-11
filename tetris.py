#!/usr/bin/env python3
import pygame # library to generate the graphic interface
import numpy as np # library to handle matrices
# from math import floor # import this function
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
        self.DBLUE = (0, 153, 255)
        self.LBLUE = (102, 255, 255)
        self.PINK = (255, 0, 255)
        self.GREEN = (102, 255, 102)
        self.YELLOW = (255, 255, 102)
        self.ORANGE = (255, 102, 0)
        self.RED = (255, 80, 80)
    def RANDOM(self):
        colorSet = dict(self.__dict__)
        for x in ["BG", "GRID", "WHITE", "BLACK"]: del colorSet[x] # Remove not wanted colors
        list = [colorSet[colorTitle] for colorTitle in [colorTitle for colorTitle in colorSet]]
        return list[np.random.randint(len(list))]

def getCubeCoord(x, y, *smaller): # Returns the same coordinates with the margin frame
    smallerC = (sizeWidthX / 15) if smaller else 0 
    center = 1 if smaller else 0
    rawCoord = [ # get coord of the cornes of the square
        (x * sizeWidthX + smallerC + center, y * sizeWidthY + smallerC + center),
        ((x + 1) * sizeWidthX - smallerC, y * sizeWidthY + smallerC + center),
        ((x + 1) * sizeWidthX - smallerC, (y + 1) * sizeWidthY - smallerC),
        (x * sizeWidthX + smallerC + center, (y + 1) * sizeWidthY - smallerC)
    ]
    return [tuple(map(lambda i: i + marginFrame, tu)) for tu in rawCoord]

# -------------     CLASSES      -------------

class tetrisPiece:
    def __init__(self):
        self.color = COLOR.RANDOM() # Get color
        # self.type = type # Store type
        self.pieces = [] # Here the pieces will be stored
        # Straight: |   Square:   |   T:        |   L:        |   L':       |   Skew:     |   Skew':
        # 0 0 0 0   |   - 0 0 -   |   - 0 - -   |   - - 0 -   |   0 - - -   |   - 0 0 -   |   0 0 - -
        # - - - -   |   - 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 - -   |   - 0 0 -
        self.type = np.random.randint(7) 
        print(self.getTypeName() + " piece created")
        
        if self.type == 0: # "Straight"
            self.pieces = [block(i, 0, self.color)for i in range(4)]
        elif self.type == 1: # "Square"
            self.pieces = [block(i + 1, j, self.color)for i in range(2) for j in range(2)]
        elif self.type == 2: # "T"
            self.pieces = [block(i, 1, self.color)for i in range(3)] + [block(1, 0, self.color)]
        elif self.type == 3: # "L"
            self.pieces = [block(i, 1, self.color)for i in range(3)] + [block(2, 0, self.color)]
        elif self.type == 4: # "L'"
            self.pieces = [block(i, 1, self.color)for i in range(3)] + [block(0, 0, self.color)]
        elif self.type == 5: # "Skew"
            self.pieces = [block(i, 1, self.color)for i in range(2)] + [block(i + 1, 0, self.color)for i in range(2)]
        elif self.type == 6: # "Skew'"
            self.pieces = [block(i, 0, self.color)for i in range(2)] + [block(i + 1, 1, self.color)for i in range(2)]

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
    
    def fall(self):
        for b in self.pieces:
            b.y = b.y + 1
    
    def canFall(self):
        for b in self.pieces:
            if not b.validBlock(0, 1) or grid[b.x, b.y + 1] != None: # If someone below:
                return False
        return True 

    def validRotation(self, blocks):
        for b in blocks:
            if not b.validBlock():
                return False
        return True

    def rotate(self):
        if self.type == 0: # "Straight"
            if self.pieces[0].y == self.pieces[1].y: # Horizontal position
                print("hori")
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(-2, 2, 1):
                    print(i)
                    self.pieces[i + 2].x = ini[0]
                    self.pieces[i + 2].y = ini[1] + i
            else:
                print("vertical")
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(-2, 2, 1):
                    self.pieces[i + 2].x = ini[0] + i
                    self.pieces[i + 2].y = ini[1]
        # elif self.type == 2: # "T"
        # elif self.type == 3: # "L"
        # elif self.type == 4: # "L'"
        elif self.type == 5: # "Skew":
            if self.pieces[0].y == self.pieces[1].y: # Horizontal position
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(2):
                    self.pieces[i].x = ini[0] - 1
                    self.pieces[i].y = ini[1] - 1 + i
                self.pieces[3].x = ini[0]
                self.pieces[3].y = ini[1] + 1
            else:
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(2):
                    self.pieces[i].x = ini[0] - 1 + i
                    self.pieces[i].y = ini[1] + 1
                self.pieces[3].x = ini[0] + 1
                self.pieces[3].y = ini[1]

        elif self.type == 6: # "Skew'":
            if self.pieces[0].y == self.pieces[1].y: # Horizontal position
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(2):
                    self.pieces[i].x = ini[0] + 1
                    self.pieces[i].y = ini[1] - 1 + i
                self.pieces[3].x = ini[0]
                self.pieces[3].y = ini[1] + 1
            else:
                ini = [self.pieces[2].x, self.pieces[2].y]
                for i in range(2):
                    self.pieces[i].x = ini[0] - 1 + i
                    self.pieces[i].y = ini[1] - 1
                self.pieces[3].x = ini[0] + 1
                self.pieces[3].y = ini[1]


    def typeConv(self): # to convert a int to the equivalent piece
        return ["Straight", "Square", "T", "L", "L'", "Skew", "Skew'"]
    
    def getTypeName(self):
        return self.typeConv()[int(self.type)]

class block:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c

    def validBlock(self, x = 0, y = 0):
        return self.x + x >= 0 and self.x + x < sizeX and self.y + y >= 0 and self.y + y < sizeY

# -------------     CODE      -------------


pygame.init() # Init pygame
pygame.display.set_caption("Jkutkut's Tetris") # Set the title of the game

# CONSTANTS
score, level = 0, 0
currentPiece, nextPiece = None, None
width = 500 
sizeX, sizeY = 14, 20 # Number of cell spots in each axis (horizontal, vertical)
height = int(sizeY * width / sizeX)
extraWidth = 300 # Some space to display the score, level, next piece...
marginFrame = 20
sizeWidthX = width / sizeX # Size of each spot
sizeWidthY = height / sizeY
COLOR = color() # Get the color class with the constants


screen = pygame.display.set_mode((width + extraWidth + 2 * marginFrame, height + 2 * marginFrame)) # Set the size of the window

font = pygame.font.Font('freesansbold.ttf', 32) 
scoreLabel = font.render('Score:', False, COLOR.WHITE) 
levelLabel = font.render('Level:', False, COLOR.WHITE) 


# State of the cells: None = empty, else = filled
grid = np.matrix([[None for j in range(sizeY)] for i in range(sizeX)])
currentPiece = tetrisPiece()
nextPiece = tetrisPiece()
currentPiece.start()

for i in range(sizeX-1):
    grid[i, 19] = COLOR.RANDOM()

lastGameTick = time.process_time() # store when we started
gameRunning = True # If false, the game stops
# timeRunning = False # If true, time runs (so iterations occur)
while gameRunning:
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
    screen.blit(font.render(str(level), False, COLOR.WHITE), ((18.5 - (len(str(score))-1)/4) * sizeWidthX, 10 * sizeWidthY))


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
        score = score + validRows * 100 + (validRows - 1) * 100

    pygame.display.flip() # Update the screen
    
    if time.process_time() - lastGameTick > 0.25: # Update the screen but game ticks every some period 
        lastGameTick = time.process_time() # Update current game tick
        if(currentPiece.canFall()):
            currentPiece.fall()
        else:
            for b in currentPiece.pieces:
                grid[b.x, b.y] = b.color
            currentPiece = nextPiece
            nextPiece = tetrisPiece()
            currentPiece.start()

    for event in pygame.event.get(): # for each event
        if event.type == pygame.QUIT: # if quit btn pressed
            gameRunning = False # no longer running game
        elif event.type == pygame.KEYDOWN:
            if event.key == 32: # Space pressed
                # timeRunning = not timeRunning # Togle the run of iterations
                while currentPiece.canFall(): currentPiece.fall()
            elif event.key == 273: # Arrow up
                score = score + 10
            elif event.key == 274: # Arrow down
                # currentPiece.move(0, -1)
                currentPiece.rotate()
            elif event.key == 275: # Arrow right
                currentPiece.move(1, 0)
            elif event.key == 276: # Arrow left
                currentPiece.move(-1, 0)
            print(event.key)
    

    # gameRunning = False

print("Thanks for playing, I hope you liked it.")
print("See more projects like this one on https://github.com/jkutkut/")
pygame.quit() # End the pygame