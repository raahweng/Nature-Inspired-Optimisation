import random
import math
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt

population = []
pointnum = 25
popnum = 500
parents = 50
k = 2
g = 9.8

for j in range(popnum):
    temp = []
    temp.append(20)
    for i in range(pointnum-2):
        temp.append(random.uniform(0,20))
    temp.append(10)
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
                time += (2 * math.sqrt((20/pointnum) ** 2 + dy ** 2))/(v1 + math.sqrt(v1 ** 2 + 2*g*dy))
            except ZeroDivisionError:
                time += 1000
            v1 = math.sqrt(v1 ** 2 + 2*g*dy)
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
##    newpop.append(population[0])
    for i in range(popnum):
        pair = (random.randint(0,parents-1), random.randint(0,parents-1))
        points = random.sample(range(1,pointnum-1), k)
        points.insert(0, 0)
        points.append(pointnum)
        points.sort()
        temp = []
        for j in range(k+1):
            temp = temp + population[pair[j%2]][points[j]:points[j+1]]       
        for j in range(pointnum):
            chance = random.uniform(1,pointnum)
            if chance >= pointnum-1 and j > 0 and j < pointnum-1:
                temp[j] = random.uniform(0,20)
        newpop.append(temp)
    return newpop
  

dxlist = []
for i in range(pointnum):
  dxlist.append(i*10/pointnum*2)

for i in range(10000):
	args = fitness(population)
	population = offspring(args[0], args[1])

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
