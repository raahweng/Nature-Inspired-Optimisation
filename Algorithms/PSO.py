import numpy as np
import random

psize = 60
cp = 2
cg = 2
wmax = 0.5
wmin = 0.5

position, velocity, pbest, gbest = 0,0,0,0

def f(population, fobj, bounds, N, ite, maxite):
    global position, velocity, pbest, gbest, wmax, wmin

    w=wmax-(wmax-wmin)*ite/maxite
    for i in range(psize):
        for j in range(N):
            rp, rg = random.random(), random.random()
            velocity[i][j] = w*velocity[i][j] + cp*rp*(pbest[i][j]-position[i][j]) + cg*rg*(gbest[j]-position[i][j])
        position[i] += velocity[i]
        
        if fobj(position[i]) < fobj(pbest[i]):
            pbest[i] = position[i]
            if fobj(pbest[i]) < fobj(gbest):
                gbest = pbest[i]

    return position
            

def initialise(bounds,N, fobj, maxite):
    global position, velocity, pbest, gbest

    position = np.zeros((psize, N))
    velocity = np.zeros((psize, N))
    pbest = np.zeros((psize, N))
    gbest = np.zeros((N,1))

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

