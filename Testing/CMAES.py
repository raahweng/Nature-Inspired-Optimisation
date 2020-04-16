import numpy as np
import random
import cma
import math
es = 0
popsize = 30

def f(population, fobj, bounds, N, ite, maxnfe):
    global es
    #Use CMA-ES ask-and-tell interface to manually perform one iteration
    population = es.ask()
    es.tell(population, [fobj(x) for x in population])
    return np.array(population)

def initialise(bounds,N,fobj, maxnfe):
    global es
    #Initialise CMA-ES object from library with initial random seed, initial std 10 and bounds to positive real numbers
    population = np.random.uniform(bounds[0], bounds[1], N)
    es = cma.CMAEvolutionStrategy(population, 10)
    return population

def name():
    return "CMA-ES"

def nfe(ite):
    #NFE per iteration is the CMA-ES lambda, calculated using no. of dimensions
    N = 25
    return (4 + math.floor(3*math.log(N))) * ite