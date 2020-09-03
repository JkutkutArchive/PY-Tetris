#!/usr/bin/env python3
import pygame # library to generate the graphic interface
import numpy as np # library to handle matrices
import time # to set a delay between each iteration

pygame.init() # Init pygame
pygame.display.set_caption("Jkutkut's Tetris") # Set the title of the game

screen = pygame.display.set_mode((500,400)) # Set the size of the window

lastGameTick = time.process_time()

focus = 2

while True:
    for event in pygame.event.get():
        if (event.type == pygame.ACTIVEEVENT and event.state == 2):
            if event.gain == 0:
                print("lost focus")
            elif event.gain == 1:
                print("focus")