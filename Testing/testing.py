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
    elif np.shape(population)[1] == 1:
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
        if abs(fit - minima[fobjstr]) < tol:
            break
        population = alg.f(population, fobj, bounds[fobjstr], N, ite, maxnfe)
        ite += 1
        nfe += nfeinc
        fit = fittest(population, fobj)
        hist.append(fit)
    #plt.plot(range(0,nfe+nfeinc, nfeinc), hist)
    #plt.show()
    return hist

# counter = 0
# for i in range(100):
#     hist = test(BA, t.dropwave, "dropwave", 5, 10000, 1e-5)
#     print(abs(hist[-1] - minima["dropwave"]))
#     if len(hist) >= 10000/BA.nfe(1)+1:
#         counter += 1
#     else:
#         pass
# print(counter)

#test(SA, t.sphere, "sphere", 10, 10000, 1e-3)

# import scipy.optimize
# alg = scipy.optimize.minimize(t.michalewicz, np.random.uniform(bounds["michalewicz"][0], bounds["michalewicz"][1], (2,1)), method="BFGS")
# sol = alg.x
# print(alg)




def testadd(alg, fobj, fobjstr, N, maxnfe, tol):
    trials = []
    for i in range(100):
        population = alg.initialise(bounds[fobjstr], N, fobj, maxnfe)
        fit = fittest(population, fobj)
        start = fit
        nfe = 0
        nfeinc = alg.nfe(1)
        ite = 0
        while True:
            if nfe >= maxnfe:
                break
            if abs(fit - minima[fobjstr]) < tol:
                break
            population = alg.f(population, fobj, bounds[fobjstr], N, ite, maxnfe)
            ite += 1
            nfe += nfeinc
            fit = fittest(population, fobj)
        trials.append([nfe, start, fit])
    return trials

    
def testset(alg, filename):
    data = []
    data.append(testadd(alg, t.sphere, "sphere", 2, 10000, 1e-3))
    data.append(testadd(alg, t.bartelsconn, "bartelsconn", 2, 10000, 1e-3))
    data.append(testadd(alg, t.dropwave, "dropwave", 2, 10000, 1e-3))
    data.append(testadd(alg, t.easom, "easom", 2, 10000, 1e-3))
    data.append(testadd(alg, t.michalewicz, "michalewicz", 2, 10000, 1e-3))
    data.append(testadd(alg, t.schwefel, "schwefel", 2, 10000, 1e-3))
    data.append(testadd(alg, t.rastrigin, "rastrigin", 5, 10000, 1e-3))
    data.append(testadd(alg, t.sphere, "sphere", 10, 10000, 1e-3))
    data.append(testadd(alg, t.rotatedhe, "rotatedhe", 10, 10000, 1e-3))
    data.append(testadd(alg, t.ackley, "ackley", 10, 10000, 1e-3))
    data.append(testadd(alg, t.rosenbrock, "rosenbrock", 10, 10000, 1e-3))
    data.append(testadd(alg, t.zakharov, "zakharov", 10, 10000, 1e-3))
    data.append(testadd(alg, t.step, "step", 10, 10000, 1e-3))
    pickle.dump(data, open( filename, "wb" ))

testset(GA, "GA.p")
testset(DE, "DE.p")
testset(CMAES, "CMAES.p")
testset(SA, "SA.p")
testset(PSO, "PSO.p")
testset(BA, "BA.p")

# for i in pickle.load( open( "BA.p", "rb" )):
#     print(i)



