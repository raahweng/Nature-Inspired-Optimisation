import numpy as np
import random
import cma
es = 0
popsize = 30

def f(population, fobj, bounds, N):
    global es
    population = es.ask()
    es.tell(population, [fobj(x) for x in population])
    return population

def initialise(bounds,N):
    global es
    population = np.random.uniform(bounds[0], bounds[1], N)
    es = cma.CMAEvolutionStrategy(population, 10, {'bounds': [0,np.inf]})
    return population

def name():
    return ("CMA-ES")