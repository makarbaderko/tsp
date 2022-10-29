import random
import math
from colorama import Fore, Style
import matplotlib.pyplot as plt
import numpy as np
import copy
import collections

class Salesman:
    global cities
    def __init__(self):
        self.genome = []
        self.score = 0
    def __lt__(self, other):
        return self.score < other.score
 
    def __gt__(self, other):
        return self.score > other.score
    def update(self):
        self.score = score(self.genome, cities)

def read_graph(path : str) -> list:
    """
    str path: path to the file wich will be read
    This function reads the coordinates of graph's vertices.
    Sample file: 
    2 2
    3 4
    5 6
    8 9
    return list data: [[2, 2], [3, 4]]
    """
    print("Reading the data")
    data = []
    with open(path) as f:
        while True:
            line = f.readline().split()
            if not line:
                break
            if len(line) == 2:
                data.append(line)
            elif len(line) == 3:
                data.append([line[1], line[2]])
    print("Data was read succefully")
    return data

def mutate(genome : list) -> list:
    """
    str genome: route of the salesman by the point number in list of cities ("0123450")
    This function creates a mutation in the genome, swapping 2 cities randomly
    First and last city is always same, so we swap genes in genome[:-1]
    """
    initial = genome.copy()
    while True:
        city1 = random.randint(0, len(genome) - 2) # - 1 for indexation from 0, - 1 for endstop
        city2 = random.randint(0, len(genome) - 2)
        if city1 == city2:
            continue
        break
    tmp = genome[city1]
    genome[city1] = genome[city2]
    genome[city2] = tmp
    genome[-1] = genome[0]
    # print(f"{len(initial) == len(genome)}")
    return genome

def distance(pointA : list, pointB : list) -> float:
    """
    HELPER FUNCTION
    Calculate cartesian distance from point A to point B
    :param pointA: [xa, ya]
    :param pointB: [xb, yb]
    return float √(xb - xa)^2 + (yb - ya)^2
    """
    return math.sqrt((int(pointB[0]) - int(pointA[0]))**2 + (int(pointB[1]) - int(pointA[1]))**2)


def score(genome : list, data : list) -> float:
    """
    Score the TSP problem solution
    """
    score = 0
    for i in range(0, len(genome) - 2):
        score += distance(data[i], data[i+1])
    return score


def rotate(arr, n):
    r_arr = collections.deque(arr)
    r_arr.rotate(len(arr) - n - 1)
    r_arr = list(r_arr)
    return r_arr

def crossover(p1, p2, with_rotate = False, with_placement = False):
    c1 = [0] * len(p1)
    
    numbers = random.sample(range(1, len(p1) - 1), 2)
    numbers.sort()
    [a, b] = numbers
    [a, b] = [2, 4]

    for e in range(a, b + 1):
        c1[e] = p1[e]
        
    rem = list(set(p2) - set(c1))

    new_rem = []
    p2_r = rotate(p2, b) if with_rotate else p2
    for el in p2_r:
        if el in rem:
            new_rem.append(el)

    print("cutoff", f"{a}:{b}", p1[a:b+1], b - a)
    print("remaining", new_rem)

    i = b + 1 if with_placement else 0
    for el in p2_r:
        if el in new_rem:
            c1[i] = el
            if with_placement:
                end_of_array = i == len(p2) - 1
                i = 0 if end_of_array else i + 1
            else:
                cutoff = i == (a - 1)
                i = b + 1 if cutoff else i + 1

    return c1

def show_genome(genome : list, cities : list) -> None:
    """
    This function plots the genome graph
    """
    fig, ax = plt.subplots()
    for city in cities:
        ax.plot(int(city[0]), int(city[1]), "ro")
    for i in range(0, len(genome) - 2):
        ax.plot([int(cities[int(genome[i])][0]), int(cities[int(genome[i+1])][0])], [int(cities[int(genome[i])][1]), int(cities[int(genome[i+1])][1])])
    plt.plot()
    plt.title(f"Genome score={score(genome, cities)}")
    plt.show()

def create_population(size : int, cities : list) -> list:
    population = []
    for i in range(size):
        genome = []
        while len(genome) != len(cities):
            city = str(random.randint(0, len(cities) - 1))
            if city in genome:
                continue
            genome.append(city)
        genome.append(genome[0])
        new = Salesman()
        new.genome = genome
        new.update()
        population.append(new)
    return population
def genetic_algorithm(cities : list) -> Salesman:
    """
    Main function
    """
    POPULATION_SIZE = 100
    EPOCHS = 200
    ELITISM_RATE = 2
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.1
    TOURNAMENT_SELECTION_RATE = 4
    MATING_RATE = 0.5
    TARGET = 100
    population = create_population(POPULATION_SIZE, cities)
    print("New salesmen were born")
    for salesman in population:
        print(Fore.RED + f"Genome {'|'.join(salesman.genome[:10])}...,", end='')
        print(Fore.GREEN +  f"Score {salesman.score}")
  
    #Main loop
    for generation in range(EPOCHS):
        new_population = []
        #Elitism
        for i in range(0, ELITISM_RATE):
            new_population.append(sorted(population)[i])
        for i in range(math.floor(MATING_RATE * len(population))):
            #Crossover
            if random.random() < CROSSOVER_RATE:
                parent1 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_RATE)
                )[0]

                parent2 = sorted(
                    random.choices(population, k=TOURNAMENT_SELECTION_RATE)
                )[0]

                child_genome = crossover(parent1.genome, parent2.genome)
                print(child_genome)
                print(len(child_genome))
                print(len(cities))
                child = Salesman()
                child.genome = child_genome
                child.update()
            else:
                child = random.choice(population)
            #Mutation
            if random.random() < MUTATION_RATE:
                child.genome = mutate(child.genome)
            child.update()
            new_population.append(child)
        population = new_population
        if generation % 10 == 0:
            print(Fore.RED + f"Generation: {generation}", end =' ')
            print(Fore.GREEN + f"Best Score: {sorted(population)[0].score}")
            #print(Fore.GREEN + f"Best Genome: {sorted(population)[0].genome}")
        if sorted(population)[0].score < TARGET:
            break
    return sorted(population)[0]

if __name__ == '__main__':
    cities = read_graph('data.txt')
    print(len(cities))
    best_salesman = genetic_algorithm(cities)
    show_genome(best_salesman.genome, cities)
    print("Execution Finished")
    print(Style.RESET_ALL)
