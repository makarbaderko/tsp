import random
import math

class Salesman:
    def __init__(self):
        self.genome = ""
        self.score = 0

def read_graph(path):
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
            line = f.readline()
            if not line:
                break
            data.append(line.split())
    print("Data was read succefully")
    return data

def mutate(genome):
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

def init_genome(cities):
    """
    list n_cities: list of cities in the TSP problem
    """
    genome = ""
    while len(genome) != len(cities):
        city = str(random.randint(0, len(cities)))
        if city in genome:
            continue
        genome += city
    genome += genome[0]
    return genome

def distance(pointA, pointB):
    """
    HELPER FUNCTION
    Calculate distance from point A to point B
    AB = √(xb - xa)^2 + (yb - ya)^2
    """
    return math.sqrt((int(pointB[0]) - int(pointA[0]))**2 + (int(pointB[1]) - int(pointA[1]))**2)

def score(genome, data):
    """
    Score the TSP problem solution
    """
    score = 0
    for i in range(0, len(genome) - 2):
        score += distance(data[i], data[i+1])
    return score

def genetic_algorithm(cities):
    """
    Main function
    """
    POPULATION_SIZE = 100
    population = []
    newSalesman = Salesman()
    for i in range(POPULATION_SIZE):
        newSalesman.genome = init_genome(cities)
        newSalesman.score = score(newSalesman.genome, cities)
        population.append(newSalesman)
    print("New salesmen were born")
    for salesman in population:
        print(f"Genome {salesman.genome}, Score {salesman.score}")

if __name__ == '__main__':
    cities = read_graph('data.txt')
    genetic_algorithm(cities)