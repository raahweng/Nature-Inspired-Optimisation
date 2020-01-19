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
    time = 0
    v1 = 0
    for j in range(pointnum-1):
      dy = abs(population[i][j+1]-population[i][j])
      try:
        time += (2 * math.sqrt((20/pointnum) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2+2*9.8*dy))
      except ZeroDivisionError:
        time += 1000000000000000
      v1 = math.sqrt(v1 ** 2+2*9.8*dy)
    times.append(time)
    print(times[0])
  return population[times.index(min(times))]

def offspring(parent):
  population = []
  population.append(parent)
  for i in range(popnum-1):
    temp = []
    temp.append(20)
    for j in range(pointnum-2):
      chance = random.uniform(1,pointnum)
      if chance >= pointnum-1:
          temp.append(random.uniform(0,20))
      else:
        temp.append(parent[j+1])
    temp.append(10)
    population.append(temp)
  return population
  

dxlist = []
for i in range(pointnum):
  dxlist.append(i*10/pointnum*2)

for i in range(1000):
  population = offspring(fitness(population))
plt.plot(dxlist, fitness(population))
plt.show()


print(population)




    
