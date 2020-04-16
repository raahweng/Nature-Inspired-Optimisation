import sys, random, time, cma, importlib, matplotlib, pickle
import numpy as np
import matplotlib.pyplot as plt

#Import algorithms and functions
GA = importlib.import_module("GA")
DE = importlib.import_module("DE")
CMAES = importlib.import_module("CMAES")
PSO = importlib.import_module("PSO")
SA = importlib.import_module("SA")
BA = importlib.import_module("BA")
t = importlib.import_module("testfunc")
bounds = t.funcbounds()
minima = t.fminima()


def fittest(population, fobj):
    if len(np.shape(population)) == 1:
        return fobj(population)
    else:
        return min([fobj(i) for i in population])


def test(alg, fobj, fobjstr, N, maxnfe, tol):
    population = alg.initialise(bounds[fobjstr], N, fobj, maxnfe)
    fit = fittest(population, fobj)
    hist = [fit]
    nfe = 0
    nfeinc = alg.nfe(1)
    ite = 0
    while True:
        if nfe >= maxnfe:
            break
        if fit - minima[fobjstr] < tol:
            break
        population = alg.f(population, fobj, bounds[fobjstr], N, ite, maxnfe)
        ite += 1
        nfe += nfeinc
        fit = fittest(population, fobj)
        hist.append(fit)
    #plt.plot(range(0,nfe+nfeinc, nfeinc), hist)
    #plt.show()
    return hist

def testset(alg, filename):
    data = []
    for i in range(2):
        data.append(test(alg, t.sphere, "sphere", 2, 10000, 1e-10))
        data.append(test(alg, t.bartelsconn, "bartelsconn", 2, 10000, 1e-10))
        data.append(test(alg, t.dropwave, "dropwave", 2, 10000, 1e-10))
        data.append(test(alg, t.easom, "easom", 2, 10000, 1e-10))
        data.append(test(alg, t.sphere, "sphere", 10, 10000, 1e-10))
        data.append(test(alg, t.rotatedhe, "rotatedhe", 10, 10000, 1e-10))
        data.append(test(alg, t.ackley, "ackley", 10, 10000, 1e-10))
        data.append(test(alg, t.schwefel, "schwefel", 10, 10000, 1e-10))
        data.append(test(alg, t.rastrigin, "rastrigin", 10, 10000, 1e-10))
        data.append(test(alg, t.rosenbrock, "rosenbrock", 10, 10000, 1e-10))
        data.append(test(alg, t.zakharov, "zakharov", 10, 10000, 1e-10))
        data.append(test(alg, t.michalewicz, "michalewicz", 10, 10000, 1e-10))
        data.append(test(alg, t.step, "step", 10, 10000, 1e-10))
    pickle.dump(data, open( filename, "wb" ))

testset(GA, "GA.p")
print(len(pickle.load( open( "GA.p", "rb" ) )))

#test(BA, t.sphere, "sphere", 2, 10000, 1e-10)


