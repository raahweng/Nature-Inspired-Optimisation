import numpy as np
import math, random, time

nbat = 30
A0 = 0.5
r0 = 0.9
qmin = 0
qmax = 0.02
q,v, S = 0,0,0
best,fitness = 0,0



def f(population, fobj, bounds, N, ite, maxnfe):
    global best, fitness, q, v, fmin, A, r, S
    q = (qmin + (qmax-qmin))*np.random.random((nbat, N))
    v += (population-best)*q
    S += v
    S = np.clip(S, bounds[0], bounds[1])
    for i in range(nbat):
        if random.random()>r[i]:
            S[i] = best + np.random.uniform(-1, 1, (1,N))*np.sum(A)/nbat
            S[i] = np.clip(S[i], bounds[0], bounds[1])
    for i in range(nbat):
        fnew = fobj(S[i])
        if fnew <= fitness[i] and random.random()<A[i]:
            population[i] = S[i]
            fitness[i] = fnew
            A[i] = A[i] * 0.9
            r[i] *= (1-np.exp(-0.9*ite))
        if fnew <= fmin:
            best = S[i]
            fmin = fnew
    return population
                

def initialise(bounds,N,fobj,maxnfe):
    global best, fitness, fmin, q, v, S, A, r
    population = np.random.normal(0, 1, (nbat, N))
    fitness = [fobj(x) for x in population]
    fmin = min(fitness)
    best = population[fitness.index(fmin)]
    q = np.zeros((nbat,1))
    v = np.zeros((nbat,N))
    S = np.zeros((nbat,N))
    A = np.full((nbat,1), A0)
    r = np.full((nbat,1), r0)
    return population


def name():
    return "Bat Algorithm"

def nfe(ite):
    return nbat * ite