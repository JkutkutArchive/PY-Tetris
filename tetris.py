#!/usr/bin/env python3
import pygame # library to generate the graphic interface
import numpy as np # library to handle matrices
from math import floor # import this function
import time # to set a delay between each iteration


# -------------     FUNCTIONS AND CLASSES      -------------

def constant(f): #define of a constant class
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class color():
    def __init__(self):
        self.BG = (255, 255, 255)
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

class tetrisPiece:
    def __init__(self, type):
        self.color = COLOR.RANDOM() # Get color
        self.type = type # Store type
        self.pieces = [] # Here the pieces will be stored
        # Straight: |   Square:   |   T:        |   L:        |   L':       |   Skew:
        # 0 0 0 0   |   - 0 0 -   |   - 0 - -   |   - - 0 -   |   0 - - -   |   - 0 0 -
        # - - - -   |   - 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 0 -   |   0 0 - -

        # if self.typeConv[self.type] == "Straight":
        #     for i in range(4):
        #         self.pieces = self.pieces + [()]
        # elif self.typeConv[self.type] == "Square":
        # elif self.typeConv[self.type] == "T":
        # elif self.typeConv[self.type] == "L":
        # elif self.typeConv[self.type] == "Skew":

    @constant
    def typeConv(self): # to convert a int to the equivalent piece
        return ["Straight", "Square", "T", "L", "L'" "Skew"]

class bloq:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c

# -------------     CODE      -------------


pygame.init() # Init pygame
pygame.display.set_caption("Jkutkut's Tetris") # Set the title of the game

# CONSTANTS
score, level = 0, 0
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
scoreLabel = font.render('Score:', False, COLOR.BLACK) 
levelLabel = font.render('Level:', False, COLOR.BLACK) 


# State of the cells: None = empty, else = filled
grid = np.matrix([[None for j in range(sizeY)] for i in range(sizeX)])

for i in range(sizeX-1):
    grid[i, 5] = COLOR.RANDOM()

gameRunning = True # If false, the game stops
# timeRunning = False # If true, time runs (so iterations occur)
while gameRunning:
    screen.fill(COLOR.BG) # Clean screen
    
    # newGrid = np.copy(grid) # Make a copy of the grid
    for x in range(sizeX): # for each spot in the grid
        for y in range(sizeY):
            # Draw the grid
            pygame.draw.polygon(screen, COLOR.GRID, getCubeCoord(x, y), 1)
            if(grid[x, y] != None):
                pygame.draw.polygon(screen, grid[x, y], getCubeCoord(x, y, True), 0)
    
    for x in range(4):
        for y in range(2):
            pygame.draw.polygon(screen, COLOR.GRID, getCubeCoord(x + 16, y + 1), 1)

    screen.blit(scoreLabel, (17.25 * sizeWidthX, 5 * sizeWidthY))
    screen.blit(font.render(str(score), False, COLOR.BLACK), ((18.5 - (len(str(score))-1)/4) * sizeWidthX, 6 * sizeWidthY))

    screen.blit(levelLabel, (17.25 * sizeWidthX, 9 * sizeWidthY))
    screen.blit(font.render(str(level), False, COLOR.BLACK), ((18.5 - (len(str(score))-1)/4) * sizeWidthX, 10 * sizeWidthY))


    pygame.display.flip() # Update the screen

    # Check rows to add score and remove rows
    validRows = 0
    for y in range(sizeY):
        valid = True
        for x in range(sizeX):
            if grid[x, y] == None:
                valid = False
                break
        if valid:
            validRows = validRows + 1
            for x in range(sizeX):
                grid[x, y] = None
    if validRows > 0:
        score = score + validRows * 100 + (validRows - 1) * 50


    for event in pygame.event.get(): # for each event
        if event.type == pygame.QUIT: # if quit btn pressed
            gameRunning = False # no longer running game
        elif event.type == pygame.KEYDOWN:
            if event.key == 32: # Space pressed
                timeRunning = not timeRunning # Togle the run of iterations
            elif event.key == 273: # Arrow up
                score = score + 10
            elif event.key == 274: # Arrow down
                score = score - 1
            print(event.key)

print("Thanks for playing, I hope you liked it.")
print("See more projects like this one on https://github.com/jkutkut/")
pygame.quit() # End the pygame