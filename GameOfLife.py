import numpy as np
import random
import argparse
import pygame
import sys

pygame.init()

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
ALIVE = [255,0,32]
DEAD = [0,255,255]
 
# This sets the margin between each cell
MARGIN = 1

def add_glider(i, j, grid):
    glider = np.array([[0,0,255], [255,0,255], [0,255,255]])
    grid[i:i+3, j:j+3] = glider

def random_grid(N):
    return np.random.choice([255, 0], N*N, p=[0.2, 0.8]).reshape(N, N)

def update(grid, N, screen):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation
            # takes place on a toroidal surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + grid[(i-1)%N, j] + grid[(i+1)%N, j] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            
            # apply Conway's rules
            if grid[i, j] == 255:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
                    pygame.draw.rect(screen, DEAD, [(MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN, WIDTH, HEIGHT])
            else:
                if total == 3:
                    newGrid[i, j] = 255
                    pygame.draw.rect(screen, ALIVE, [(MARGIN + WIDTH) * j + MARGIN, (MARGIN + HEIGHT) * i + MARGIN, WIDTH, HEIGHT])


    # update data
    grid[:] = newGrid[:]

def main():
    parser = argparse.ArgumentParser(description ="Runs Conway's Game of Life simulation")
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    N = 100

    if args.N and int(args.N) > 8:
        N = int(args.N)
    
    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    grid = np.array([])

    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        add_glider(1, 1, grid)
    else:
        grid = random_grid(N)

    pygame.display.set_caption("The Game of Life")
    screen = pygame.display.set_mode([700, 700])
    screen.fill([0,0,0])
    clock = pygame.time.Clock()
    not_done = True
    while not_done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                not_done = False  # Flag that we are done so we exit this loop
        clock.tick(update_interval)
        update(grid, N, screen)
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    

main()