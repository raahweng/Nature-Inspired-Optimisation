import numpy as np
import random

GAlmda = 150  #Population size
GAmu = 5  #No of parents for crossover
k=2  #K-point crossover parameter
#Mutation rate decay parameters
MR1 = 0.1
MRn = 0.02

#Genetic Algorithm; samples from Uniform distribution and uses K-point crossover
def f(population, fobj, bounds, N, ite, maxite):

    #Mutation decay
    MR=MRn-(MR1-MRn)*ite/maxite

    #Selection; sort population by fitness
    times = np.array([fobj(i) for i in population])
    sort = list(reversed(times.argsort()))
    population = population[sort[::-1]]
    newpop = []

    #Elitism: add fittest individual to next generation
    newpop.append(population[0])

    #Recombination
    for i in range(1,GAlmda):

        #K-point crossover; select two random individuals and splice them alternately
        pair = (random.randint(0,GAmu-1), random.randint(0,GAmu-1))
        points = random.sample(range(1,N-1), k)
        points.insert(0, 0)
        points.append(N)
        points.sort()
        temp = []
        for j in range(k+1):
            temp = np.concatenate((temp, population[pair[j%2],points[j]:points[j+1]]))

        #Mutation; 1/N chance of randomly assigning a value to each point besides start and end       
        for j in range(N):
            r = random.uniform(0,1)
            if r < MR and j > 0 and j < N-1:
                temp[j] = random.uniform(bounds[0],bounds[1])

        newpop.append(temp)
    return np.array(newpop)

def initialise(bounds,N,fobj, maxite):
    global MR
    MR = MR1
    #Random initialisation of population
    population = np.random.uniform(bounds[0], bounds[1], (GAlmda, N))
    return population

def name():
    return "Genetic Algorithm"

def nfe(ite):
    return GAlmda * ite