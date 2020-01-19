import random

parents = 3
pointnum = 10
popnum = 10
k = 2

population = []
for i in range(popnum):
    temp = []
    for j in range(pointnum):
        temp.append(j+i*10)
    population.append(temp)
print(population)


newpop = []
for i in range(10):
    pair = (random.randint(0,parents-1), random.randint(0,parents-1))
    points = random.sample(range(1,pointnum-1), k)
    points.insert(0, 0)
    points.append(pointnum)
    points.sort()
    temp = []
    for j in range(k+1):
        temp = temp + population[pair[j%2]][points[j]:points[j+1]]
    newpop.append(temp)
print(newpop)


