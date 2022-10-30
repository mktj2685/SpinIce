import numpy as np
import matplotlib.pyplot as plt
from models.spinice import SpinIce


def plot_arrows(ax: plt.Axes, model: SpinIce):

    for x in range(model.Nx):
        for y in range(model.Ny):
            # Plot vertex as marker.
            ax.plot(x, y, marker='o', color='#000000', markerfacecolor='#ffffff', markersize=4)

            # Plot right edge as arrow.
            r = model.edges[x, 2*y]
            x_, y_, dx, dy = (x, y, 1, 0) if r == 1 else (x+1, y, -1, 0)
            ax.arrow(x_, y_, dx, dy, head_width=0.2, head_length=0.2, length_includes_head=True)

            # Plot top edge as arrow.
            t = model.edges[x, 2*y+1]
            x_, y_, dx, dy = (x, y, 0, 1) if t == 1 else (x, y+1, 0, -1)
            ax.arrow(x_, y_, dx, dy, head_width=0.2, head_length=0.2, length_includes_head=True)

if __name__ == '__main__':
    # Define lattice shape.
    # NOTE number of spins is 2 x Nx x Ny.
    Nx = 8
    Ny = 8

    # Temperature
    T = 0.01

    # Monte Carlo steps
    MCSTEP = 1000

    # Create spin-ice model.
    model = SpinIce(Nx, Ny, T, 'short-loop')
    # model = SpinIce(Nx, Ny, T, 'long-loop')

    # Create Figure and Axes.
    fig = plt.figure()
    ax = fig.add_subplot()

    # Main loop
    try:
        plt.ion()
        for i in range(MCSTEP):
            # Plot spins.
            # plt.imshow(model.edges)
            plt.cla()
            plot_arrows(ax, model)
            plt.pause(0.001)
            plt.show()

            # Execute one Monte Carlo step.
            model.mcstep()

    except KeyboardInterrupt:
        plt.ioff()
        plt.close()