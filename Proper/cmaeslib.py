import math
import cma
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

N = 20

def fitness(vector):
     vector = np.transpose(vector)
     vector[0] = 20
     vector [-1] = 10
     time = 0
     v1 = 0
     for i in range(N-1):
         dy = abs(vector[i+1]-vector[i])   #Height of one line segment
         try:
             time += (2 * math.sqrt((20/N) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2+2*9.8*dy))   #Time taken for one line segment
         except ZeroDivisionError:
             time += math.inf
         v1 = math.sqrt(v1 ** 2+2*9.8*dy)    #Final velocity set to the initial velocity of next segment
     return time


def newfitness(vector):
    vector = np.transpose(vector)
    vector[0] = 20
    vector [-1] = 10
    t = 0
    v1 = 0

    for i in range(N-1):
        dy = vector[i+1]-vector[i]
        if (v1**2 - 2*9.81*dy) < 0 and i > 0:
            t = 100
            break
        d = math.sqrt((20/N)**2 + dy**2)
        if (2*d)*(-v1 + math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy) < 0:
            t += (2*d)*(-v1 - math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy)
        else:
            t += (2*d)*(-v1 + math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy)
        v1 = math.sqrt(v1**2 - 2*9.81*dy)

    return t



#xopt, es = cma.fmin2(fitness, N * [0], 0.5)

opts = cma.CMAOptions()
opts.set('tolfun', 1e-100)
opts.set('tolfunhist', 1e-100)
#opts.set('tolx', 1e-100)
opts.set('tolstagnation', 5e3)
es = cma.CMAEvolutionStrategy(N * [0], 1, opts)
while not es.stop():
    solutions = es.ask()
    es.tell(solutions, [fitness(x) for x in solutions])
    es.disp()

dxlist = []
for i in range(N):
  dxlist.append(i*10/N*2)


plt.plot(dxlist, solutions[0])
plt.show()




