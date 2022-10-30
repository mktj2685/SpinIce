import math
import random
import numpy as np


class SpinIce:

    def __init__(
        self,
        Nx: int,
        Ny: int,
        T: float,
        sampler: str
    ) -> None:

        # Set lattice shape
        self.Nx = Nx
        self.Ny = Ny

        # Set temperature
        self.T = T

        # Define edges with Ising spins on.
        # NOTE see assets/spinice.png
        #   bonds[:, odd]  : Ising spin on vertical bonds. 1 is up-arrow, -1 is down-arrow.
        #   bonds[:, even] : Ising spin on horizontal bonds. 1 is right-arrow, -1 is left-arrow.
        self.edges = np.ones((Nx, 2*Ny), dtype=np.int8)

        # Define energy of each vertex type
        # see https://en.wikipedia.org/wiki/Ice-type_model
        self.e1 = 1.0   # type1
        self.e2 = 1.0   # type2
        self.e3 = 1.0   # type3
        self.e4 = 1.0   # type4
        self.e5 = 1.0   # type5
        self.e6 = 1.0   # type6

        if sampler == 'long-loop':
            self.sampler = self.long_loop
        elif sampler == 'short-loop':
            self.sampler = self.short_loop
        else:
            raise ValueError

    def short_loop(self) -> None:
        # Select one vertex at random.
        x = random.randint(0, self.Nx-1)
        y = random.randint(0, self.Ny-1)

        # Define some variables.
        vertices = []   # encount vertice
        edges = []      # edge with flipped arrow on
        exclude = None  # edge to exclude from flip candidates

        # Main loop
        while (x, y) not in vertices:
            # Get spins on left/top/right/bottom edges on.
            l = self.edges[x-1, 2*y]    # left
            t = self.edges[x, 2*y+1]    # top
            r = self.edges[x, 2*y]      # right
            b = self.edges[x, 2*y-1]    # bottom

            # Defince some variables.
            outgoing = []   # indices with outgoing arrows on.
            direction = []  # direction of edge from vertex with outgoing arrows on.

            # Case with outgoing arrow on left edge
            if exclude != 'left' and l == -1:
                outgoing.append((x-1, 2*y))
                direction.append('left')

            # Case with outgoing arrow on top edge
            if exclude != 'top' and t == 1:
                outgoing.append((x, 2*y+1))
                direction.append('top')
            
            # Case with outgoing arrow on right edge
            if exclude != 'right' and r == 1:
                outgoing.append((x, 2*y))
                direction.append('right')

            # Case with outgoing arrow on bottom edge
            if exclude != 'bottom' and b == -1:
                outgoing.append((x, 2*y-1))
                direction.append('bottom')

            # Choice outgoing edge and flip
            idx = random.randint(0, len(outgoing)-1)
            self.edges[outgoing[idx]] *= -1

            # Add vertex and flipped edges
            vertices.append((x, y))
            edges.append(outgoing[idx])

            # Case left edge is flipped.
            # The next vertex excludes the right edge from candidates for flip.
            if direction[idx] == 'left':
                x = (x-1) % self.Nx
                exclude = 'right'

            # Case top edge is flipped.
            # The next vertex excludes the bottom edge from candidates for flip.            
            elif direction[idx] == 'top':
                y = (y+1) % self.Ny
                exclude = 'bottom'

            # Case right edge is flipped.
            # The next vertex excludes the left edge from candidates for flip.   
            elif direction[idx] == 'right':
                x = (x+1) % self.Nx
                exclude = 'left'
            
            # Case bottom edge is flipped.
            # The next vertex excludes the top edge from candidates for flip.
            elif direction[idx] == 'bottom':
                y = (y-1) % self.Ny
                exclude = 'top'
            
            else:
                raise Exception

        # Trace backwards from the point of first encounter and flip.
        idx = vertices.index((x, y))
        for i in range(idx):
            self.edges[edges[i]] *= -1

    def long_loop(self) -> None:
        # Select one vertex at random.
        x0 = random.randint(0, self.Nx-1)
        y0 = random.randint(0, self.Ny-1)

        # Define some variables.
        exclude = None  # edge to exclude from flip candidates

        # Set current forcus vertex.
        x = x0
        y = y0

        # Main loop
        while True:
            # Get spins on left/top/right/bottom edges on.
            l = self.edges[x-1, 2*y]    # left
            t = self.edges[x, 2*y+1]    # top
            r = self.edges[x, 2*y]      # right
            b = self.edges[x, 2*y-1]    # bottom

            # Defince some variables.
            outgoing = []   # indices with outgoing arrows on.
            direction = []  # direction of edge from vertex with outgoing arrows on.

            # Case with outgoing arrow on left edge
            if exclude != 'left' and l == -1:
                outgoing.append((x-1, 2*y))
                direction.append('left')

            # Case with outgoing arrow on top edge
            if exclude != 'top' and t == 1:
                outgoing.append((x, 2*y+1))
                direction.append('top')
            
            # Case with outgoing arrow on right edge
            if exclude != 'right' and r == 1:
                outgoing.append((x, 2*y))
                direction.append('right')

            # Case with outgoing arrow on bottom edge
            if exclude != 'bottom' and b == -1:
                outgoing.append((x, 2*y-1))
                direction.append('bottom')

            # Choice outgoing edge and flip
            idx = random.randint(0, len(outgoing)-1)
            self.edges[outgoing[idx]] *= -1

            # Case left edge is flipped.
            # The next vertex excludes the right edge from candidates for flip.
            if direction[idx] == 'left':
                x = (x-1) % self.Nx
                exclude = 'right'

            # Case top edge is flipped.
            # The next vertex excludes the bottom edge from candidates for flip.            
            elif direction[idx] == 'top':
                y = (y+1) % self.Ny
                exclude = 'bottom'

            # Case right edge is flipped.
            # The next vertex excludes the left edge from candidates for flip.   
            elif direction[idx] == 'right':
                x = (x+1) % self.Nx
                exclude = 'left'
            
            # Case bottom edge is flipped.
            # The next vertex excludes the top edge from candidates for flip.
            elif direction[idx] == 'bottom':
                y = (y-1) % self.Ny
                exclude = 'top'
            
            else:
                raise Exception

            # If encout first vertex, break main loop.
            if x == x0 and y == y0:
                break

    def energy(self) -> float:
        # Initialize energy.
        e = 0.0

        # The loop run all vertices.
        for x in range(self.Nx):
            for y in range(self.Ny):
                # Get spins on left/top/right/bottom edges on.
                l = self.edges[x-1, 2*y]    # left
                t = self.edges[x, 2*y+1]    # top
                r = self.edges[x, 2*y]      # right
                b = self.edges[x, 2*y-1]    # bottom

                # Case vertex (x, y) is type1.
                if l == 1 and t == 1 and r == 1 and b == 1:
                    e += self.e1
                
                # Case vertex (x, y) is type2.
                elif l == -1 and t == -1 and r == -1 and b == -1:
                    e += self.e2
                
                # Case vertex (x, y) is type3.
                elif l == 1 and t == -1 and r == 1 and b == -1:
                    e += self.e3
                
                # Case vertex (x, y) is type4.
                elif l == -1 and t == 1 and r == -1 and b == 1:
                    e += self.e4
                
                # Case vertex (x, y) is type5.
                elif l == 1 and t == 1 and r == -1 and b == -1:
                    e += self.e5

                # Case vertex (x, y) is type6.
                elif l == -1 and t == -1 and r == 1 and b == 1:
                    e += self.e6

                else:
                    raise Exception

        return e

    def metropolis(self) -> None:
        # Set energy and edges before update.
        e0 = self.edges.copy()
        E0 = self.energy()

        # Update edges.
        self.sampler()

        # Set energy and edges after update.
        e1 = self.edges.copy()
        E1 = self.energy()
        
        # Calculate the energy difference.
        dE = E1 - E0

        # If energy decreses, accept updated edges.
        if dE < 0:
            self.edges = e1
        
        # If energy dosen't decreses, accept update edges with probabilty P = exp(-ΔE/T).
        else:
            r = random.random()
            # accept
            if r < math.exp(-dE / self.T):
                self.edges = e1
            
            # reject
            else:
                self.edges = e0

    def mcstep(self) -> None:
        self.metropolis()


if __name__ == '__main__':
    # Define lattice shape.
    # NOTE number of spins is 2 x Nx x Ny.
    Nx = 16
    Ny = 16

    # Temperature
    T = 0.01

    # Create spin-ice model.
    model = SpinIce(Nx, Ny, T, 'short-loop')
    # model = SpinIce(Nx, Ny, T, 'long-loop')

    # Main loop
    for i in range(100):
        model.mcstep()
