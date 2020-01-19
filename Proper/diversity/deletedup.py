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
    for i in range(len(population)):
        time = 0
        v1 = 0
        for j in range(pointnum-1):
            dy = abs(population[i][j+1]-population[i][j])
            try:
                time += (2 * math.sqrt((20/pointnum) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2 + 2*9.8*dy))
            except ZeroDivisionError:
                time += 1000
            v1 = math.sqrt(v1 ** 2 + 2*9.8*dy)
        times[i][0] = time
    return population, times

def offspring(population, times, generation):
    newpop = []
    times.sort()
    newpop.append(population[0])
    print(times[0][0])
    mean = []
    for i in range(pointnum):
        val = 0
        for j in range(popnum):
            val += population[j][i]
        val /= popnum
        mean.append(val)
    diversity = []
    for i in range(popnum):
        val = 0
        for j in range(pointnum):
            val += abs(mean[j]-population[i][j])
        val /= pointnum
        diversity.append(val)
    mean_div = sum(diversity)/popnum
    for i in range(len(population)):
        if abs(diversity[i]-mean_div) < 0.15: #(5 ** (1/((generation+1) ** 0.25)))/10:
            times[i][0] = 1000
              
    times.sort()
    order = []
    for i in range(popnum):
        order.append(times[i][1])
    population = [population[i] for i in order]
    for i in range(popnum-1):
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
##            if j > 0 and j < pointnum-1:
##              temp[j] += numpy.random.normal(0, 0.1)
##              if temp[j] > 20:
##                temp[j] = 20
##              elif temp[j] < 0:
##                temp[j] = 0
        newpop.append(temp)
    return newpop
  

dxlist = []
for i in range(pointnum):
  dxlist.append(i*10/pointnum*2)

for i in range(5000):
    args = fitness(population)
    population = offspring(args[0], args[1], i)

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
