import random
import math
from colorama import Fore, Style
import matplotlib.pyplot as plt


class Salesman:
    def __init__(self):
        self.genome = []
        self.score = 0
    def __lt__(self, other):
        return self.score < other.score
 
    def __gt__(self, other):
        return self.score > other.score

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
    return genome

def init_genome(cities : list) -> list:
    """
    list n_cities: list of cities in the TSP problem
    """
    genome = []
    while len(genome) != len(cities):
        city = str(random.randint(0, len(cities) - 1))
        if city in genome:
            continue
        genome .append(city)
    genome.append(genome[0])
    return genome

def distance(pointA : list, pointB : list) -> float:
    """
    :type
    HELPER FUNCTION
    Calculate cartesian distance from point A to point B
    list pointA: [xa, ya]
    list pointB: [xb, yb]
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

def breed(genome1, genome2):
    child = []
    childP1 = []
    childP2 = []
    geneA = int(random.random() * len(genome1))
    geneB = int(random.random() * len(genome1))
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    for i in range(startGene, endGene):
        childP1.append(genome1[i])
    childP2 = [item for item in genome2 if item not in childP1]
    child = childP1 + childP2
    return child

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
def genetic_algorithm(cities : list) -> Salesman:
    """
    Main function
    """
    POPULATION_SIZE = 100
    EPOCHS = 1000
    ELITISM_RATE = 2
    CROSSOVER_RATE = 0.8
    MUTATION_RATE = 0.1
    TOURNAMENT_SELECTION_RATE = 4
    MATING_RATE = 0.5
    TARGET = 100
    population = []
    for i in range(POPULATION_SIZE):
        population.append(Salesman())
        population[-1].genome = init_genome(cities)
        population[-1].score = score(population[-1].genome, cities)
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
                parent1 = sorted(random.choices(population, k=TOURNAMENT_SELECTION_RATE))[0] #Getting the best from the random pool of salesman of size k.
                parent2 = sorted(random.choices(population, k=TOURNAMENT_SELECTION_RATE))[0]
                child = Salesman()
                child.genome = breed(parent1.genome, parent2.genome)
                child.score = score(child.genome, cities)
            else:
                child = random.choice(population)
            #Mutation
            if random.random() < MUTATION_RATE:
                child.genome = mutate(child.genome)
            child.score = score(child.genome, cities)
            child.score = score(child.genome, cities)
            new_population.append(child)
        population = new_population
        print(Fore.RED + f"Generation: {generation}", end =' ')
        print(Fore.GREEN + f"Best Score: {sorted(population)[0].score}")
        #print(Fore.GREEN + f"Best Genome: {sorted(population)[0].genome}")
        if sorted(population)[0].score < TARGET:
            break
    return sorted(population)[0]

if __name__ == '__main__':
    cities = read_graph('data.txt')
    best_salesman = genetic_algorithm(cities)
    show_genome(best_salesman.genome, cities)
    print("Execution Finished")
    print(Style.RESET_ALL)