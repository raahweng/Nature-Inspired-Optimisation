import sys, random, time, cma, importlib, matplotlib, pickle, math
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
#     hist = test(CMAES, t.dropwave, "dropwave", 2, 10000, 1e-3)
#     print(abs(hist[-1] - minima["dropwave"]))
#     if len(hist) >= 10000/CMAES.nfe(1)+1:
#         counter += 1
#     else:
#         pass
# print(counter)

#test(SA, t.sphere, "sphere", 10, 10000, 1e-3)

# import scipy.optimize
# alg = scipy.optimize.basinhopping(t.michalewicz, np.random.uniform(bounds["michalewicz"][0], bounds["michalewicz"][1], (5,1)))
# alg = scipy.optimize.shgo(t.michalewicz, [(bounds["michalewicz"][0], bounds["michalewicz"][1]) for i in range(5)])
# alg = scipy.optimize.dual_annealing(t.michalewicz, [(bounds["michalewicz"][0], bounds["michalewicz"][1]) for i in range(5)])
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
        success = False
        nfesuccess = 0
        while True:
            if nfe >= maxnfe:
                break
            if abs(fit - minima[fobjstr]) < tol and success == False:
                success = True
                nfesuccess = nfe
            population = alg.f(population, fobj, bounds[fobjstr], N, ite, maxnfe)
            ite += 1
            nfe += nfeinc
            fit = fittest(population, fobj)
        trials.append([nfesuccess, success, start, fit])
    return trials

    
def testset(alg, filename):
    data = []
    data.append(testadd(alg, t.sphere, "sphere", 2, 10000, 1e-3))
    data.append(testadd(alg, t.bartelsconn, "bartelsconn", 2, 10000, 1e-3))
    data.append(testadd(alg, t.dropwave, "dropwave", 2, 10000, 1e-3))
    data.append(testadd(alg, t.easom, "easom", 2, 10000, 1e-3))
    data.append(testadd(alg, t.michalewicz, "michalewicz", 5, 10000, 1e-3))
    data.append(testadd(alg, t.schwefel, "schwefel", 2, 10000, 1e-3))
    data.append(testadd(alg, t.rastrigin, "rastrigin", 5, 10000, 1e-3))
    data.append(testadd(alg, t.rosenbrock, "rosenbrock", 5, 10000, 1e-3))
    data.append(testadd(alg, t.sphere, "sphere", 10, 10000, 1e-3))
    data.append(testadd(alg, t.rotatedhe, "rotatedhe", 10, 10000, 1e-3))
    data.append(testadd(alg, t.ackley, "ackley", 10, 10000, 1e-3))
    data.append(testadd(alg, t.zakharov, "zakharov", 10, 10000, 1e-3))
    data.append(testadd(alg, t.step, "step", 10, 10000, 1e-3))
    pickle.dump(data, open( filename, "wb" ))

testset(GA, "GA.p")
testset(DE, "DE.p")
testset(CMAES, "CMAES.p")
testset(SA, "SA.p")
testset(PSO, "PSO.p")
testset(BA, "BA.p")


# for i, j in enumerate(pickle.load( open( "CMAES.p", "rb" ))):
#     accuracy = 0
#     counter = 0
#     for k in j:
#         if k[0] < 10000:
#             counter += 1
#             if k[2]-list(minima.values())[i] == 0:
#                 accuracy += math.log10(sys.float_info.min)
#             else:
#                 try:
#                     accuracy += math.log10(abs(k[2]-list(minima.values())[i])) - math.log10(abs(k[1]-list(minima.values())[i]))
#                 except:
#                     print("HELP")
#                     print(list(minima.values())[i])
#     if counter > 0:
#         accuracy /= counter
#     else:
#         accuracy = "N/A"
#     print(accuracy)



