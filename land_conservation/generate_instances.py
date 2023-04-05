
import random
import numpy as np
from math import floor, ceil
def generate_land_conservation_problem(n_species, width, height, budget_factor, seed=0):

    random.seed(seed)
    np.random.seed(seed)

    population_range = [2,3,4]
    set_population = [10,15,20]
    threshold = [0.3, 0.5, 0.7]

    max_radius_city = 4
    n_cities = random.randrange(1,3)
    max_radius_lake = 3
    n_lakes= random.randrange(1, 4)
    max_radius_forest = 7
    n_forests = random.randrange(5, 7)


    grid_species = []
    species_threshold = []

    for specie in range(n_species):
        n_populations = random.choice(population_range)
        animals_in_grid = np.zeros(shape=(width, height), dtype=int)
        for population in range(n_populations): # each species can have several populations
            x = random.randrange(width)
            y = random.randrange(height)
            std = np.random.uniform(0.8, 1.8)
            qty = random.choice(set_population) # number of animals in grid cell (x,y)
            distribution = np.random.multivariate_normal(mean=(x,y), cov=[[std, 0], [0, std]], size=qty)
            for i,j in distribution:
                if i < width and j < height:
                    animals_in_grid[floor(i), floor(j)] += 1

        grid_species.append(animals_in_grid)
        species_threshold.append(int(random.choice(threshold) * animals_in_grid.sum()))

    grid_cost = np.ones(shape=(width,height), dtype=int)

    city_cost = 15
    for _ in range(n_cities):
        city_width = random.randrange(1, max_radius_city)
        city_height = random.randrange(1, max_radius_city)
        x,y = random.randrange(0,width-1), random.randrange(0, height-1)
        city = grid_cost[x: x+city_width,y: y+city_height]
        city[city < city_cost] = city_cost

    lake_cost = 5
    for _ in range(n_lakes):
        lake_radius = random.randrange(1, max_radius_lake)
        lake_center = np.array([random.randrange(0, width-1), random.randrange(0, height-1)])

        # loop over all cells, can probably be done better...
        for i in range(width):
            for j in range(height):
                dist = np.linalg.norm(lake_center - np.array([i,j]))
                if dist <= lake_radius and grid_cost[i,j] < lake_cost:
                    grid_cost[i,j] = lake_cost


    forest_cost = 12
    for _ in range(n_forests):
        forest_radius = random.randrange(1, max_radius_forest)
        forest_center = np.array([random.randrange(0, width - 1), random.randrange(0, height - 1)])
        std = 2

        x,y = forest_center
        # loop over all cells, can probably be done better...
        for i in range(width):
            for j in range(height):
                dist = np.linalg.norm(forest_center - np.array([i, j]))
                cost = forest_cost * np.exp(-((i - x) ** 2 + (j - y) ** 2) / std ** 2)
                if dist <= forest_radius and grid_cost[i, j] < cost:
                    grid_cost[i, j] = cost

    print(grid_cost)

    budget = ceil(grid_cost.mean() * (width + height) * budget_factor)

    return {"n_species":n_species,
            "grid_species": grid_species,
            "grid_cost": grid_cost,
            "species_threshold":species_threshold,
            "budget": budget}