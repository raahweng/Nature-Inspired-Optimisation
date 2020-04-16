import numpy as np
import random

DElmda = 0  #Population size
F = 0.8  # Differential Weight; Range 0-2; Recommended value 0.8
CR = 0.9  # Crossover Rate; Range 0-1; Recommended value 0.9

#Differential Evolution
def f(population, fobj, bounds, N, ite, maxnfe):

    for i in range(DElmda):

        #Select 3 individuals from population; Mutate one by the weighted difference of the other two; Clip mutant to constraints
        sample = list(range(DElmda))
        sample.remove(i)
        abc = random.sample(sample, 3)
        mutant = population[abc[0]] + F * (population[abc[1]]-population[abc[2]])
        np.clip(mutant, bounds[0], bounds[1])

        #Mutate each value in the mutant to the individual's value according to Crossover Rate
        for j in range(N):
            r = random.uniform(0,1)
            if r > CR:
                mutant[j] = population[i][j]
        #Replace individual with mutant if fitter
        if fobj(mutant) < fobj(population[i]):
            population[i] = mutant
        
    return population

def initialise(bounds,N,fobj, maxnfe):
    global DElmda
    DElmda = 15
    #Random initialisation of population
    population = np.random.uniform(bounds[0], bounds[1], (DElmda, N))
    return population

def name():
    return "Differential Evolution"

def nfe(ite):
    return 2 * DElmda * ite