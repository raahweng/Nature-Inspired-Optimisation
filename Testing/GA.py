import numpy as np
import random
import time

GAlmda = 0  #Population size
GAmu = 0  #No of parents for crossover
k=2  #K-point crossover parameter
#Mutation rate decay parameters
MR1 = 0.3
MRn = 0.01
MR = 0
#Mutation magnitude parameters
M1 = 0
Mn = 1e-6
M = 0

#Genetic Algorithm; samples from Uniform distribution and uses K-point crossover
def f(population, fobj, bounds, N, ite, maxnfe):
    global MR, M
    #Mutation decay
    MR *= (MRn/MR1)**(nfe(1)/(maxnfe-1))
    M *= (Mn/M1)**(nfe(1)/(maxnfe-1))

    #Selection; sort population by fitness
    fitnesses = np.array([fobj(i) for i in population])
    sort = list(reversed(fitnesses.argsort()))
    population = population[sort[::-1]]
    newpop = []

    #Elitism: add fittest individual to next generation
    newpop.append(population[0])

    #Recombination
    for i in range(1,GAlmda):

        #K-point crossover; select two random individuals and splice them alternately
        pair = (random.randint(0,GAmu-1), random.randint(0,GAmu-1))
        if N > 2:
            points = random.sample(range(1,N-1), k)
            points.insert(0, 0)
            points.append(N)
            points.sort()
            temp = []
            for j in range(k+1):
                temp = np.concatenate((temp, population[pair[j%2],points[j]:points[j+1]]))
        else:
            temp = [population[pair[0]][0],population[pair[1]][1]]
        

        #Mutation; 1/N chance of randomly assigning a value to each point besides start and end       
        for j in range(N):
            r = random.uniform(0,1)
            if r < MR:
                temp[j] += np.random.normal(0,M)
                np.clip(temp[j], bounds[0], bounds[1])

        newpop.append(temp)
    return np.array(newpop)

def initialise(bounds,N,fobj, maxnfe):
    global MR, GAlmda, GAmu, MR1, MRn, M, M1
    GAlmda = N*10 
    GAmu = np.floor(0.25 * GAlmda)
    #Random initialisation of population
    population = np.random.uniform(bounds[0], bounds[1], (GAlmda, N))
    if N == 2:
        MR1 = 1
        MRn = 0.75
    MR = MR1
    M1 = abs(bounds[0]-bounds[1])
    M = M1
    return population

def name():
    return "Genetic Algorithm"

def nfe(ite):
    return GAlmda * ite