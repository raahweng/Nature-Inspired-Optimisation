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
basinhop = importlib.import_module("basinhop")
dualanneal = importlib.import_module("dualanneal")
ampgo = importlib.import_module("ampgo")
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
    plt.plot(range(0,nfe+nfeinc, nfeinc), hist)
    plt.show()
    return hist

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

# testset(GA, "GA.p")
# testset(DE, "DE.p")
# testset(CMAES, "CMAES.p")
# testset(SA, "SA.p")
# testset(PSO, "PSO.p")
# testset(BA, "BA.p")


# for i in pickle.load( open( "BA.p", "rb" )):
#     success = 0
#     nfe = 0
#     for j in i:
#         if j[1] == True:
#             success += 1
#             nfe += j[0]
#     if success > 0:
#         nfe /= success
#         print(nfe)
#     else:
#         print("N/A")
    

# for i, j in enumerate(pickle.load( open( "BA.p", "rb" ))):
#     accuracy = 0
#     counter = 0
#     for k in j:
#         if k[1] == True:
#             counter += 1
#             if k[3]-list(minima.values())[i] == 0:
#                 accuracy += math.log10(sys.float_info.min)
#             else:sys
#                 try:
#                     accuracy += math.log10(abs(k[3]-list(minima.values())[i])) - math.log10(abs(k[2]-list(minima.values())[i]))
#                 except:
#                     print("HELP")
#                     print(list(minima.values())[i])
#     if counter > 0:
#         accuracy /= counter
#     else:
#         accuracy = "N/A"
#     print(accuracy)



def bhtest(fobj, fobjstr, N, maxnfe=10000, tol=1e-3):
    results = []
    for i in range(100):
        start = np.random.uniform(bounds[fobjstr][0], bounds[fobjstr][1], (N,1))
        alg = basinhop.basinhopping(fobj, start, 100, 1, 0.5, {"bounds":[(bounds[fobjstr][0], bounds[fobjstr][1]) for i in range(N)], "tol":sys.float_info.min}, minima[fobjstr])
        results.append([alg.nfesuccess, alg.success, fobj(start), alg.fun, alg.nfev])
    return results

def bhtestset():
    data = []
    data.append(bhtest(t.sphere, "sphere", 2))
    data.append(bhtest(t.bartelsconn, "bartelsconn", 2))
    data.append(bhtest(t.dropwave, "dropwave", 2))
    data.append(bhtest(t.easom, "easom", 2))
    data.append(bhtest(t.michalewicz, "michalewicz", 5))
    data.append(bhtest(t.schwefel, "schwefel", 5))
    data.append(bhtest(t.rastrigin, "rastrigin", 5))
    data.append(bhtest(t.rosenbrock, "rosenbrock", 5))
    data.append(bhtest(t.sphere, "sphere", 10))
    data.append(bhtest(t.rotatedhe, "rotatedhe", 10))
    data.append(bhtest(t.ackley, "ackley", 10))
    data.append(bhtest(t.zakharov, "zakharov", 10))
    data.append(bhtest(t.step, "step", 10))
    pickle.dump(data, open( "basinhop.p", "wb" ))


def datest(fobj, fobjstr, N, maxnfe=10000, tol=1e-3):
    results = []
    for i in range(100):
        start = np.random.uniform(bounds[fobjstr][0], bounds[fobjstr][1], N)
        alg = dualanneal.dual_annealing(fobj, [(bounds[fobjstr][0], bounds[fobjstr][1]) for i in range(N)], (), 10000, {"tol":sys.float_info.min}, 5230, 2e-05, 2.62, -5, 10000, None, False, None, start, minima[fobjstr])
        results.append([alg.nfevsuccess, alg.success, fobj(start), alg.fun, alg.nfev])
    return results


def datestset():
    data = []
    data.append(datest(t.sphere, "sphere", 2))
    data.append(datest(t.bartelsconn, "bartelsconn", 2))
    data.append(datest(t.dropwave, "dropwave", 2))
    data.append(datest(t.easom, "easom", 2))
    data.append(datest(t.michalewicz, "michalewicz", 5))
    data.append(datest(t.schwefel, "schwefel", 5))
    data.append(datest(t.rastrigin, "rastrigin", 5))
    data.append(datest(t.rosenbrock, "rosenbrock", 5))
    data.append(datest(t.sphere, "sphere", 10))
    data.append(datest(t.rotatedhe, "rotatedhe", 10))
    data.append(datest(t.ackley, "ackley", 10))
    data.append(datest(t.zakharov, "zakharov", 10))
    data.append(datest(t.step, "step", 10))
    pickle.dump(data, open( "dualanneal.p", "wb" ))

# bhtestset()
# datestset()


# for i in pickle.load( open( "dualanneal.p", "rb" )):
#     success = 0
#     nfe = 0
#     for j in i:
#         if j[1] == True:
#             success += 1
#             nfe += j[0]
#     if success > 0:
#         nfe /= success
#         print(success, nfe)
#     else:
#         print("N/A")
# for i, j in enumerate(pickle.load( open( "dualanneal.p", "rb" ))):
#     accuracy = 0
#     counter = 0
#     for k in j:
#         if k[1] == True:
#             counter += 1
#             if k[3]-list(minima.values())[i] == 0:
#                 accuracy += math.log10(sys.float_info.min)
#             else:
#                 try:
#                     accuracy += math.log10(abs(k[3]-list(minima.values())[i])) - math.log10(abs(k[2]-list(minima.values())[i]))
#                 except:
#                     print("HELP")
#                     print(list(minima.values())[i])
#     if counter > 0:
#         accuracy /= counter
#     else:
#         accuracy = "N/A"
#     print(accuracy)


def ampgotest(fobj, fobjstr, n):
    results = []
    for i in range(100):
        x0 = np.random.uniform(bounds[fobjstr][0],bounds[fobjstr][1],(n,1))
        bound = [(bounds[fobjstr][0],bounds[fobjstr][1]) for i in range(n)]
        xf, yf, fun_evals, msg, tt,nfesuccess,succ = ampgo.AMPGO(fobj, x0, (), "L-BFGS-B", None, bound, 10000, 1000, 5, 1e-5, 0.02, 0.01 ,5, 'oldest', minima[fobjstr], None)
        results.append([nfesuccess, succ, x0, yf])
    return results

def ampgotestset():
    data = []
    data.append(ampgotest(t.sphere, "sphere", 2))
    data.append(ampgotest(t.bartelsconn, "bartelsconn", 2))
    data.append(ampgotest(t.dropwave, "dropwave", 2))
    data.append(ampgotest(t.easom, "easom", 2))
    data.append(ampgotest(t.michalewicz, "michalewicz", 5))
    data.append(ampgotest(t.schwefel, "schwefel", 5))
    data.append(ampgotest(t.rastrigin, "rastrigin", 5))
    data.append(ampgotest(t.rosenbrock, "rosenbrock", 5))
    data.append(ampgotest(t.sphere, "sphere", 10))
    data.append(ampgotest(t.rotatedhe, "rotatedhe", 10))
    data.append(ampgotest(t.ackley, "ackley", 10))
    data.append(ampgotest(t.zakharov, "zakharov", 10))
    data.append(ampgotest(t.step, "step", 10))
    pickle.dump(data, open( "ampgo.p", "wb" ))

# for i, j in enumerate(pickle.load( open( "ampgo.p", "rb" ))):
#     accuracy = 0
#     counter = 0
#     for k in j:
#         if k[1] == True:
#             counter += 1
#             if k[3]-list(minima.values())[i] == 0:
#                 accuracy += math.log10(sys.float_info.min)
#             else:
#                 try:
#                     accuracy += math.log10(abs(k[3]-list(minima.values())[i])) - math.log10(abs(k[2]-list(minima.values())[i]))
#                 except:
#                     print("HELP")
#                     print(list(minima.values())[i])
#     if counter > 0:
#         accuracy /= counter
#     else:
#         accuracy = "N/A"
#     print(accuracy)


index = 12
accuracy = 0
counter = 0
nfe = 0
for c, i in enumerate(pickle.load( open( "ampgo.p", "rb" ))[index]):
    if i[1] == True:
        counter += 1
        nfe += i[0]
        start = t.step(i[2])
        if i[3]-list(minima.values())[index] == 0:
            accuracy += math.log10(sys.float_info.min)
        else:
            accuracy += math.log10(abs(i[3]-list(minima.values())[index])) - math.log10(abs(start-list(minima.values())[index]))
print(counter)
print(nfe/counter)
print(accuracy/counter)
