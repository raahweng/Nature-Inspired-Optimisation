import numpy as np
import math, random, time

cycles = 250
p1 = 0.4
pn = 0.001
xc, fc = 0,0
t1 = -1/math.log(p1)
tn = -1/math.log(pn)
t=t1
deltaE_avg, deltaE = 0,0
na = 0
frac = 0

def f(population, fobj, bounds, N, ite, maxite):
    global xc,fc,t,na,deltaE_avg,deltaE

    if ite == 0:
        xc = population

    for i in range(cycles):
        mutant = population + np.random.normal(0,abs(bounds[0]-bounds[1])**0.3,(N,1))
        fmutant = fobj(mutant)
        deltaE = abs(fmutant-fc)
        accept = False
        if fmutant < fc:
            if ite == 0:
                deltaE_avg = deltaE
            p = math.exp(-deltaE/(deltaE_avg * t))
            accept = random.random() > p
        if accept:
            xc = mutant
            fc = fmutant
            na += 1
            deltaE_avg = (deltaE_avg*(na-1)+ deltaE)/na
    population = xc
    t *= frac
    return population
    

def initialise(bounds,N,fobj,maxite):
    global xc,fc, frac
    population = np.random.uniform(bounds[0], bounds[1], (N,1))
    xc = population
    fc = fobj(population)
    frac = (tn/t1)**(1/(maxite-1))
    return population

def name():
    return "Simulated Annealing"

