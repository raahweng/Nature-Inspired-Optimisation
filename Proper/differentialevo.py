import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

pointnum = 25
popnum = 25
population = np.zeros([popnum, pointnum])
F = 0.8 ## 0-2 #0.8 #0.25
CR = 0.9 ## 0-1 #0.9 #0.55
fitgraph = []

for i in range(popnum):
    population[i][0] = 20
    for j in range(pointnum-2):
        population[i][j + 1] = random.uniform(0,20)
    population[i][pointnum-1] = 10

def fitness(alist):
    time = 0
    v1 = 0
    for i in range(pointnum-1):
        dy = abs(alist[i+1]-alist[i])
        try:
            time += (2 * math.sqrt((20/pointnum) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2+2*9.8*dy))
        except ZeroDivisionError:
            time += math.inf
        v1 = math.sqrt(v1 ** 2+2*9.8*dy)
    return time

def recombinate(population):
    for i in range(popnum):
        sample = list(range(popnum))
        sample.remove(i)
        abc = random.sample(sample, 3)
        mutant = population[abc[0]] + F * (population[abc[1]]-population[abc[2]])
        np.clip(mutant, 0, 20)
        for j in range(pointnum):
            r = random.uniform(0,1)
            if r > CR:
                mutant[j] = population[i][j]
        if fitness(mutant) < fitness(population[i]):
            population[i] = mutant
    return population

for i in range(1000):
    population = recombinate(population)
    my_min = math.inf
    index = -1
    for j in range(pointnum):
        if fitness(population[j]) < my_min:
            my_min = fitness(population[j])
            index = j
    fitgraph.append(fitness(population[index]))
    print(str(fitness(population[index])) + "   " + str(i))

dxlist = []
for i in range(pointnum):
  dxlist.append(i*10/pointnum*2)


plt.plot(dxlist, population[index])
plt.show()
plt.plot(fitgraph)
plt.show()



