import sys, random, time, cma, math, scipy
from scipy.optimize import *
import numpy as np

#Toggle Values
N = 10 #Dimensions, ie No. of Points
#Genetc Algorit0m
GAlmda = 100
GAmu = 5
k=2
#Differential Evolution
DElmda = 100
F = 0.25 ## 0-2 #0.8 #0.25
CR = 0.5 ## 0-1 #0.9 #0.55

def GA(population, fobj, bounds):
    times = np.array([fobj(i) for i in population])
    sort = list(reversed(times.argsort()))
    population = population[sort[::-1]]
    newpop = []
    newpop.append(population[0])
    for i in range(1,GAlmda):
        pair = (random.randint(0,GAmu-1), random.randint(0,GAmu-1))
        points = random.sample(range(1,N-1), k)
        points.insert(0, 0)
        points.append(N)
        points.sort()
        temp = []
        for j in range(k+1):
            temp = np.concatenate((temp, population[pair[j%2],points[j]:points[j+1]]))       
        for j in range(N):
            chance = random.uniform(1,N)
            if chance >= N-1 and j > 0 and j < N-1:
                temp[j] = random.uniform(bounds[0],bounds[1])
        newpop.append(temp)
    return np.array(newpop)
  

def DE(population, fobj, bounds):
    global N, DElmda, F, CR
    for i in range(DElmda):
        sample = list(range(DElmda))
        sample.remove(i)
        abc = random.sample(sample, 3)
        mutant = population[abc[0]] + F * (population[abc[1]]-population[abc[2]])
        np.clip(mutant, bounds[0], bounds[1])
        for j in range(N):
            r = random.uniform(0,1)
            if r > CR:
                mutant[j] = population[i][j]
        if fobj(mutant) < fobj(population[i]):
            population[i] = mutant
    return population

#bounds [-5.12,5.12]
def sphere(x):
    return sum(x ** 2)

#bounds [-5.12,5.12]
def rastrigin(x):
    return 10*N + sum([(i**2 - 10 * np.cos(2 * math.pi * i)) for i in x])

#bounds [-32.768, 32.768]
def ackley(x):
	firstSum = 0.0
	secondSum = 0.0
	for i in x:
		firstSum += i**2.0
		secondSum += math.cos(2.0*math.pi*i)
	return -20.0*math.exp(-0.2*math.sqrt(firstSum/N)) - math.exp(secondSum/N) + 20 + math.e

#bounds [-5,10]
def rosenbrock(x):
    return sum(100.0*(x[1:] - x[:-1]**2.0)**2.0 + (1 - x[:-1])**2.0)

# sol = []
# for j in range(10):
#     GApop = np.random.uniform(-5.12, 5.12, (GAlmda,N))
#     for i in range(500):
#         GApop = GA(GApop, [-5.12,5.12])
#     sol.append(fitness(GApop[0]))
#     print(j)
# print(np.std(sol))
# print(sol)

def eval(alg, popsize, fobj, bounds):
    sol1000 = []
    sol500 = []
    for j in range(100):
        if alg != "cma":
            population = np.random.uniform(bounds[0], bounds[1], popsize)
            for i in range(1000):
                population = alg(population, fobj, bounds)
                if i == 499:
                    sol500.append(fobj(population[0]))
        else:
            es = cma.CMAEvolutionStrategy(np.random.uniform(bounds[0], bounds[1],(N,1)), 0.5)
            for i in range(1000):
                population = es.ask()
                es.tell(population, [fobj(x) for x in population])
                if i == 499:
                    sol500.append(fobj(population[0]))
        sol1000.append(fobj(population[0]))
        print(j)
    print(population[0])
    print("Standard Error: " + str(np.std(sol500)))
    print("Accuracy: " + str(sum(sol500)/10))
    with open('results.txt', 'a') as f:
        f.write("\n" + str(np.std(sol500)) + " " + str(sum(sol500)/10))
    print("Standard Error: " + str(np.std(sol1000)))
    print("Accuracy: " + str(sum(sol1000)/10))
    with open('results.txt', 'a') as f:
        f.write("\n" + str(np.std(sol1000)) + " " + str(sum(sol1000)/10))


#eval(GA, (GAlmda,N), sphere, [-5.12,5.12])
#eval(DE, (DElmda,N), sphere, [-5.12,5.12])
#eval("cma", None, sphere, [-5.12,5.12])

#eval(GA, (GAlmda,N), ackley, [-32.768, 32.768])
#eval(DE, (DElmda,N), ackley, [-32.768, 32.768])
#eval("cma", None, ackley, [-32.768, 32.768])

#eval(GA, (GAlmda,N), rastrigin, [-5.12,5.12])
#eval(DE, (DElmda,N), rastrigin, [-5.12,5.12])
#eval("cma", None, rastrigin, [-5.12,5.12])

#eval(GA, (GAlmda,N), rosenbrock, [-5,10])
#eval(DE, (DElmda,N), rosenbrock, [-5,10])
#eval("cma", None, rosenbrock, [-5,10])

#opt, es = cma.fmin2(ackley, np.random.uniform(-32.768, 32.768,(N,1)), 1)




