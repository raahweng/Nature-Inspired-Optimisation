import random
import math
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt

population = []
pointnum = 25
popnum = 12
parents = 3

for j in range(popnum):
    temp = []
    for i in range(pointnum):
        temp.append(random.uniform(0,20))
    population.append(temp)

def fitness(population):
    times = []
    for i in range(popnum):
        times.append([100, i])
    for i in range(popnum):
        time = 0
        v1 = 0
        for j in range(pointnum-1):
            dy = abs(population[i][j+1]-population[i][j])
            try:
                time += (2 * math.sqrt((20/pointnum) ** 2 + dy ** 2))/(v1 + math.sqrt(v1 ** 2 + 2*9.8*dy))
            except ZeroDivisionError:
                time += 1000
            v1 = math.sqrt(v1 ** 2 + 2*9.8*dy)
        times[i][0] = time
    return population, times

def offspring(population, times):
    order = []
    times.sort()
    print(times[0][0])
    for i in range(len(times)):
        order.append(times[i][1])
    population = [population[i] for i in order]
    newpop = []
    for i in range(popnum):
        temp = []
        temp.append(20)
        for j in range(pointnum-1):
            chance = random.uniform(1,pointnum)
            if chance >= pointnum-0.5:
                temp.append(random.uniform(0,20))
            else:
                upper = 0
                lower = 0
                for k in range(parents):
                    lower = upper
                    upper += (pointnum/(parents*(parents+1)/2))*(k+1)
                    if lower <= chance <= upper:
                        temp.append(population[parents-k][j+1])
        temp.append(10)
        newpop.append(temp)
    newpop.append(population[0])
    return newpop
  

dxlist = []
for i in range(pointnum):
  dxlist.append(i*10/pointnum*2)

for i in range(100000):
	args = fitness(population)
	population = offspring(args[0], args[1])

print(len(population))

my_min = 1001
index = -1
for i in args[1]:
    if i[0] < my_min:
        my_min = i[0]
        index = i[1]
fittest = args[0][index]

print(args[1][index])

plt.plot(dxlist, fittest)
plt.show()
