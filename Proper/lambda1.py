import random
import math
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt

population = []

for j in range (12):
  temp = []
  for i in range(25):
    temp.append(random.uniform(0,20))
  population.append(temp)

def fitness(population):
  times = []

  for i in range(12):
    time = 0
    v1 = 0
    for j in range(25-1):
      dy = population[i][j+1]-population[i][j]
      try:
        time += (math.sqrt((10/25) ** 2 + dy ** 2))/(v1+math.sqrt(v1+2*9.8*population[i][j]))
      except ZeroDivisionError:
        time += 1000000000000000
      v1 = math.sqrt(v1+2*9.8*population[i][j])
    times.append(time)
  print(times)
  return population[times.index(min(times))]

def offspring(parent):
  population = []
  for i in range(12):
    temp = []
    temp.append(20)
    for j in range(25-2):
      y = numpy.random.normal(0.0, 0.02)+parent[j+1]     #change Gaussian width
      if y >= 20:
        temp.append(20)
      elif y <= 0:
        temp.append(0)
      else:
        temp.append(y)
    temp.append(10)
    population.append(temp)
  return population
  

dxlist = []
for i in range(25):
  dxlist.append(i*10/25*2)

for i in range(2000):
  population = offspring(fitness(population))
plt.plot(dxlist, fitness(population))
plt.show()


print(population)




    
