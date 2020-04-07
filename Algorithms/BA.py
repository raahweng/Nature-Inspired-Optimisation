import numpy as np
import math, random, time

nbat=15
A1 = 0.75
An = 0.25
r1 = 0.25
rn = 0.85
A = A1
r = r1
qmin = 0
qmax = 2
q,v, S = 0,0,0
best,fitness = 0,0


def f(population, fobj, bounds, N, ite, maxite):
    global best, fitness, q, v, fmin, A, r
    A *= (An/A1)**(1/(maxite-1))
    r *= (rn/r1)**(1/(maxite-1))
    for x in range(15):
        for i in range(nbat):
            q[i] = qmin + (qmax-qmin)*random.random()
            v[i] = v[i] + (population[i]-best)*q[i]
            S[i] = population[i] + v[i]
            np.clip(S[i], bounds[0], bounds[1])
            if random.random()>r:
                S[i] = best + 0.04*np.random.uniform(bounds[0], bounds[1], (1, N))
            fnew = fobj(S[i])
            if fnew <= fitness[i] and random.random()<A:
                population[i] = S[i]
                fitness[i] = fnew
            if fnew <= fmin:
                best = S[i]
                fmin = fnew
        temp = np.where(v>500)
        for i,j in enumerate(temp[0]):
            v[j][temp[1][i]] = np.random.uniform(-250, 250)
        temp = np.where(v<-500)
        for i,j in enumerate(temp[0]):
            v[j][temp[1][i]] = np.random.uniform(-250, 250)
    return population
                

def initialise(bounds,N,fobj,maxite):
    global best, fitness, fmin, q, v, S, A, r
    A = A1
    r = r1
    population = np.random.uniform(bounds[0], bounds[1], (nbat, N))
    fitness = [fobj(x) for x in population]
    fmin = min(fitness)
    best = population[fitness.index(fmin)]
    q = np.zeros((nbat,1))
    v = np.zeros((nbat,N))
    S = np.zeros((nbat,N))
    return population


def name():
    return "Bat Algorithm"

def nfe(ite):
    return nbat * 15 * ite