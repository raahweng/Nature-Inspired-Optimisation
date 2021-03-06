import numpy as np
import math, random, time, sys


p1 = 0.98
#pn = 1e-3
xc, fc = 0,0
t1 = -1/math.log(p1)
tn =  1e-100 #-1/math.log(pn)
t=t1
deltaE_avg, deltaE = 0,0
na = 0
frac = 0
M1 = 0
Mn = 1e-2
M = 0
cycles = 1
check = False

def f(population, fobj, bounds, N, ite, maxnfe):
    global xc,fc,t,na,deltaE_avg,deltaE, M
    if ite == 0:
        xc = population
    M *= (Mn/M1)**(nfe(1)/(maxnfe-1))
    mutant = population + np.random.normal(0,M,(N,1))
    mutant = np.clip(mutant, bounds[0], bounds[1])
    if check:
        mutant = np.transpose(mutant)
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
    

def initialise(bounds,N,fobj,maxnfe):
    global xc,fc, frac, t, M1, M, check
    t = t1
    population = np.random.uniform(bounds[0], bounds[1], (N,1))
    if bounds[1] == np.pi:
        check = True
        population = np.transpose(population)
    xc = population
    fc = fobj(population)
    frac = (tn/t1)**(nfe(1)/(maxnfe-1))
    M1 = abs(bounds[0]-bounds[1])*1.5
    M = M1
    return population

def name():
    return "Simulated Annealing"

def nfe(ite):
    return ite

