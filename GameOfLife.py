import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse

def add_glider(i, j, grid):
    glider = np.array([[0,0,255], [255,0,255], [0,255,255]])
    grid[i:i+3, j:j+3] = glider

def random_grid(N):
    return np.random.choice([255, 0], N*N, p=[0.2, 0.8]).reshape(N, N)

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neghbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation
            # takes place on a toroidal surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            # apply Conway's rules
            if grid[i, j] == 255:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 255

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

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

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), frames=1000, interval = update_interval, save_count = 50)

    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['vcodec', 'libx264]'])

    print("show")
    # plt.imshow(grid, interpolation='nearest')
    plt.show()


main()