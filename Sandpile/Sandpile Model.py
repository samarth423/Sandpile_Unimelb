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
        

        
        self.load_file()

        plt.ion() 
        plt.figure(figsize = (40, 40))

        print("Starting Simulation")
        
        if self.extra_prints: self.print_sand()
        self.plot_sand()

        
        t = 0
        while t < self.T:

            self.n_iterations += 1
            if self.extra_prints: print(f"Iteration: {self.n_iterations}")

            self.n_topples = 0
           
            
            if self.randomise_drop:
                x = random.randint(0, self.M - 1)
                y = random.randint(0, self.N - 1)

            
            if not self.randomise_drop:
                x = self.M//2
                y = self.N//2

            
            self.drop_sand(x, y)
            if self.extra_prints: self.print_sand()
            self.plot_sand()

         
            while True:

                
                topple_coords = self.find_topples()
                if len(topple_coords) == 0:
                    break

                
                self.topple_the_coords(topple_coords)
                self.plot_sand()

            
            self.topple_data.append(self.n_topples)
            if self.extra_prints: print("Number of topples:",self.n_topples)

            t += 1

        
        print("Completed Simulation")
        plt.close()
        self.save_file()

        
        self.final_plot()


    def load_file(self):
        

        try:
            with open(self.filename, 'rb') as f:
                sand_dict = pickle.load(f)
                self.n_iterations = sand_dict["n_iterations"]
                self.sand_array = sand_dict["sand_array"]
                self.topple_data = sand_dict["topple_data"]
        except:
            print(f"File {self.filename} couldn't be loaded. Starting new simulation.")


    def save_file(self):
        

        if self.filename == None:
            self.filename = "sand_soc_temp.pkl"
        sand_dict = {"n_iterations": self.n_iterations, "sand_array": self.sand_array, "topple_data": self.topple_data}
        with open(self.filename, 'wb') as f:
            pickle.dump(sand_dict, f, pickle.HIGHEST_PROTOCOL)


    def drop_sand(self, x, y):
        

        if self.extra_prints: print(f"Adding to ({x}, {y})")
        self.sand_array[y][x] += 1


    def find_topples(self):
        

        topples_coords = []
        for i in range(0, self.M):
            for j in range(0, self.N):
                height  = self.sand_array[j][i]
                if height >= 4:
                    topples_coords.append([i, j])
                    self.n_topples += 1

        return topples_coords


    def topple_the_coords(self, topple_coords):
        

        for coords in topple_coords:
            x = coords[0]
            y = coords[1]

            if self.extra_prints: print(f"Toppling at ({x}, {y})")
            self.topple(x, y)
            if self.extra_prints: self.print_sand()


    def topple(self, x, y):
        

        self.sand_array[y][x] -= 4

        to_add = [] 
        if x > 0:
            to_add.append([x - 1, y])
        if x < self.M - 1:
            to_add.append([x + 1, y])
        if y > 0:
            to_add.append([x, y - 1])
        if y < self.N - 1:
            to_add.append([x, y + 1])

        while len(to_add) > 0:
            
            next_direction = to_add.pop(random.randint(0, len(to_add) - 1))

            to_add_x = next_direction[0]
            to_add_y = next_direction[1]

            self.sand_array[to_add_y][to_add_x] += 1


    def plot_sand(self):
        

        plt.imshow(self.sand_array, cmap=self.cmap, interpolation='nearest')
        plt.clim(0, self.clim)
        plt.title(f'Sandpile: Iteration {self.n_iterations}')
        plt.colorbar()

        plt.pause(self.print_pause)
        plt.clf()


    def print_sand(self):
      
        for row in self.sand_array:
            print(row)


    def final_plot(self):

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
    

    
    N = 20 # number of rows in sand array
    M = 20 # number of coloumns in sand array
    T = 20 # number of iterations

    randomise_drop = True
    starting_height = 3 
    filename = "sand_soc_1.pkl" 
    extra_prints = True

    cmap = "plasma" 
    clim = 4
    print_pause = 0.0001 

    sandpile = Sandpile(N, M, T, randomise_drop, starting_height, filename, extra_prints, cmap, clim, print_pause)
    sandpile.run()
    
