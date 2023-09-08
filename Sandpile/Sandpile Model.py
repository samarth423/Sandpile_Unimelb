import random
import matplotlib.pyplot as plt
import numpy as np
import pickle
import matplotlib.animation



class Sandpile:
   

    def __init__(self, N, M, T, randomise_drop, starting_height, filename, extra_prints, cmap, clim, print_pause):
        self.N = N
        self.M = M
        self.T = T
        self.randomise_drop = randomise_drop
        self.sand_array = np.full((self.N, self.M), starting_height, dtype=int)
        self.filename = filename
        self.extra_prints = extra_prints
        self.cmap = cmap
        self.clim = clim
        self.print_pause = print_pause

        self.n_iterations = 0
        self.n_topples = 0
        self.topple_data = []


    def run(self):
        

        # 1. Load file and data (if provided)
        self.load_file()

        plt.ion() # make plot interactive (interactable-on) e.g pausable
        plt.figure(figsize = (40, 40))

        print("Starting Simulation")
        # initial print and plot
        if self.extra_prints: self.print_sand()
        self.plot_sand()

        # 2. Begin dropping sand
        t = 0
        while t < self.T:

            self.n_iterations += 1
            if self.extra_prints: print(f"Iteration: {self.n_iterations}")

            self.n_topples = 0

            # coords to drop sand randomly
            if self.randomise_drop:
                x = random.randint(0, self.M - 1)
                y = random.randint(0, self.N - 1)

            # coords to drop sand in center
            if not self.randomise_drop:
                x = self.M//2
                y = self.N//2

            # 2.a. Drop sand
            self.drop_sand(x, y)
            if self.extra_prints: self.print_sand()
            self.plot_sand()

            # 2.b. Find and topple new unstable sand piles
            while True:

                # 2.b.i. Find them
                topple_coords = self.find_topples()
                if len(topple_coords) == 0:
                    break

                # 2.b.i. topple them
                self.topple_the_coords(topple_coords)
                self.plot_sand()

            # 2.c. Store number of topples (aka. avalanche size) for final plot
            self.topple_data.append(self.n_topples)
            if self.extra_prints: print("Number of topples:",self.n_topples)

            # 2.d. Increment iteration count
            t += 1

        # 3. Simulation complete, save the data
        print("Completed Simulation")
        plt.close()
        self.save_file()

        # 4. Plot final simulation state and power distribution curve
        self.final_plot()


    def load_file(self):
        """
        Tries to load simulation data with given filename.
        """

        try:
            with open(self.filename, 'rb') as f:
                sand_dict = pickle.load(f)
                self.n_iterations = sand_dict["n_iterations"]
                self.sand_array = sand_dict["sand_array"]
                self.topple_data = sand_dict["topple_data"]
        except:
            print(f"File {self.filename} couldn't be loaded. Starting new simulation.")


    def save_file(self):
        """
        Save simulation data with given filename or default name.
        """

        if self.filename == None:
            self.filename = "sand_soc_temp.pkl"
        sand_dict = {"n_iterations": self.n_iterations, "sand_array": self.sand_array, "topple_data": self.topple_data}
        with open(self.filename, 'wb') as f:
            pickle.dump(sand_dict, f, pickle.HIGHEST_PROTOCOL)


    def drop_sand(self, x, y):
        """
        Adds 1 sand to (x, y).
        """

        if self.extra_prints: print(f"Adding to ({x}, {y})")
        self.sand_array[y][x] += 1


    def find_topples(self):
        """
        Returns a list of coordinates of topples (i.e height >= 4)
        and increments count of topples.
        """

        topples_coords = []
        for i in range(0, self.M):
            for j in range(0, self.N):
                height  = self.sand_array[j][i]
                if height >= 4:
                    topples_coords.append([i, j])
                    self.n_topples += 1

        return topples_coords


    def topple_the_coords(self, topple_coords):
        """
        Given list of coordinates, topple them.
        """

        for coords in topple_coords:
            x = coords[0]
            y = coords[1]

            if self.extra_prints: print(f"Toppling at ({x}, {y})")
            self.topple(x, y)
            if self.extra_prints: self.print_sand()


    def topple(self, x, y):
        """
        Topples (x, y) by removing 4 sand
        and adding 1 sand to adjacents (if existing).
        """

        self.sand_array[y][x] -= 4

        to_add = [] # coords to add sand to -> [[to_add_x, to_add_y], ...]
        if x > 0:
            to_add.append([x - 1, y])
        if x < self.M - 1:
            to_add.append([x + 1, y])
        if y > 0:
            to_add.append([x, y - 1])
        if y < self.N - 1:
            to_add.append([x, y + 1])

        while len(to_add) > 0:
            # add 1 sand to adjacents
            next_direction = to_add.pop(random.randint(0, len(to_add) - 1))

            to_add_x = next_direction[0]
            to_add_y = next_direction[1]

            self.sand_array[to_add_y][to_add_x] += 1


    def plot_sand(self):
        """
        Plot sand array to screen.
        """

        plt.imshow(self.sand_array, cmap=self.cmap, interpolation='nearest')
        plt.clim(0, self.clim)
        plt.title(f'Sandpile: Iteration {self.n_iterations}')
        plt.colorbar()

        plt.pause(self.print_pause)
        plt.clf()


    def print_sand(self):
        """
        Print sand array in terminal.
        """
        for row in self.sand_array:
            print(row)


    def final_plot(self):
        """
        Plot final sand array and power-law distribution.
        """

        plt.figure(figsize = (11, 5))
        plt.subplot(121)

        plt.imshow(self.sand_array, cmap=self.cmap, interpolation='nearest')
        plt.title(f'Sandpile: Iteration {self.n_iterations}')
        plt.clim(0, self.clim)

        nped = np.array(self.topple_data)
        unique, counts = np.unique(nped, return_counts=True)

        plt.subplot(122)
        plt.scatter((unique), (counts))
        plt.title("Power-Law Distribution")
        plt.xlabel("log(s): Size of Avalanche")
        plt.ylabel("log(N(s)): Frequency of Avalanche")
        plt.yscale('log')
        plt.xscale('log')
        plt.show(block=True)



if __name__ == "__main__":
    """
    Creates a sandbox with given params. Will load and
    continue simulation if given an existing file.
    """

    # 1. Inialise Parameters (if loading a file, use the same params)
    N = 20 # number of rows in sand array
    M = 20 # number of coloumns in sand array
    T = 20 # number of iterations

    randomise_drop = True # if False, drops in center
    starting_height = 3 # starting amount of sand per point
    filename = "sand_soc_3.pkl" # filename to load and/or save data
    extra_prints = False # if True prints sand state and iteration data to terminal

    cmap = "plasma" # colourmap of plot
    clim = 4# upper limit for colourmap
    print_pause = 0.0001 # pause time between prints

    # 2. Create and run sand box!
    sandpile = Sandpile(N, M, T, randomise_drop, starting_height, filename, extra_prints, cmap, clim, print_pause)
    sandpile.run()
    