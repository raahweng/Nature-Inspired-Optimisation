import numpy as np
import random

psize = 60
cp = 1
cg = 1
wmax = 0.5
wmin = 0.5

position, velocity, pbest, gbest = 0,0,0,0

def f(population, fobj, bounds, N, ite, maxnfe):
    global position, velocity, pbest, gbest, wmax, wmin

    w=wmax-(wmax-wmin)*nfe(1)/maxnfe
    for i in range(psize):
        for j in range(N):
            rp, rg = random.random(), random.random()
            velocity[i][j] = w*velocity[i][j] + cp*rp*(pbest[i][j]-position[i][j]) + cg*rg*(gbest[j]-position[i][j])
        position[i] += velocity[i]
        np.clip(position[i], bounds[0], bounds[1])
        pfittest = fobj(pbest[i])
        pfitness = fobj(position[i])
        if pfitness < pfittest:
            pbest[i] = position[i]
            pfittest = pfitness
            if pfittest < fobj(gbest):
                gbest = pbest[i]

    return position
            

def initialise(bounds,N, fobj, maxite):
    global position, velocity, pbest, gbest

    position = np.zeros((psize, N))  #Position vector of each particle
    velocity = np.zeros((psize, N))  #Velocity vector of each particle
    pbest = np.zeros((psize, N))  #Individual best position of each particle
    gbest = np.zeros((N,1))  #Overall best position over generation

    for i in range(psize):
        position[i] = np.random.uniform(bounds[0], bounds[1], (1, N))
        pbest[i] = position[i]
        if i == 0:
            gbest = position[i]
        if fobj(position[i]) < fobj(gbest):
            gbest = position[i]
        velocity[i] = np.random.uniform(-abs(bounds[0]-bounds[1]), abs(bounds[0]-bounds[1]), (1, N))
    return position

def name():
    return "Particle Swarm Optimisation"

def nfe(ite):
    return 3 * psize * ite