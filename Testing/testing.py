import sys, random, time, cma, importlib, matplotlib
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
        if np.shape(population)[1] > 1:
            return min([fobj(i) for i in population])
        else:
            return min(fobj(population))


def test(alg, fobj, fobjstr, N, maxite, tol):
    population = alg.initialise(bounds[fobjstr], N, fobj, maxite)
    hist = []
    nfe = 0
    nfeinc = alg.nfe(1)
    for i in range(maxite):
        population = alg.f(population, fobj, bounds[fobjstr], N, i, maxite)
        nfe += nfeinc
        fit = fittest(population, fobj)
        hist.append(fit)
        if fit - minima[fobjstr] < tol:
            break
    plt.plot(hist)
    plt.show()
    return i, nfe, hist

test(GA, t.bartelsconn, "bartelsconn", 2, 200, 1e-5)