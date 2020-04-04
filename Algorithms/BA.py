import numpy as np
import math, random, time

nbat=25
A = 0.25
r = 0.5
qmin = 0
qmax = 2
q,v = 0,0

def f(population, fobj, bounds, N, ite, maxite):
    q = qmin + (qmin-qmax)*np.random.rand(nbat, 1)
    v = v + (population-fittest)*q
    S = population + v
    for i in range(nbat):
        if random.random()>r:
            S[i] = best + 0.01*np.random.uniform(bounds[0], bounds[1])
        fnew = fobj(S[i])
        if fnew<=fittest(i)
        

def initialise(bounds,N,fobj,maxite):
    population = np.random.uniform(bounds[0], bounds[1], (nbat, N))
    fitnesses = [fobj(x) for x in population]
    fmin = min(fitnesses)
    fittest = population[fitnesses.index(fmin)]
    q = np.zeros(nbat,1)
    v = np.zeros(nbat,N)


def name():
    return "Bat Algorithm"