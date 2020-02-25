import sys, pygame, random, time, cma
from scipy.optimize import newton
import numpy as np
from pygame.color import *

#Toggle Values
N = 20 #Dimensions, ie No. of Points
#Genetc Algorithm
GAlmda = 200
GAmu = 5
k=2
#Differential Evolution
DElmda = 150
F = 0.25 ## 0-2 #0.8 #0.25
CR = 0.55 ## 0-1 #0.9 #0.55

def brachistochrone(x2,y2):
    def f(theta):
        return y2/x2 - (1-np.cos(theta))/(theta-np.sin(theta))
    theta2 = newton(f, np.pi/2)
    R = y2 / (1 - np.cos(theta2))
    theta = np.linspace(0, theta2, 100)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))
    T = theta2 * np.sqrt(R / 9.8)
    return x, y, T
    

# def fitness(vector):
#     vector[0] = displayHeight-gapWidth*2
#     vector[-1] = gapWidth*2
#     t = 0
#     v1 = 0
#     for i in range(N-1):
#         try:
#             v2 = np.sqrt(v1**2 + 2*9.8*(vector[i]-vector[i+1]))
#             d = np.sqrt(((displayWidth/3-gapWidth*2)/(N-1))**2 + (vector[i]-vector[i+1])**2)
#             if vector[i+1] == vector[i]:
#                 break
#             temp = d*(v2-v1)/(vector[i]-vector[i+1])
#             if temp < 0:
#                 t = 1000
#                 break
#             else:
#                 t += temp
#                 v1 = v2
#         except:
#             t = 1000
#     t /= 9.8
#     return t

def fitness(vector):
     vector[0] = displayHeight-gapWidth*2
     vector[-1] = gapWidth*2
     time = 0
     v1 = 0
     for i in range(N-1):
         dy = abs(vector[i+1]-vector[i])
         try:
             time += (2 * np.sqrt(((displayWidth/3-gapWidth*2)/(N-1)) ** 2 + dy ** 2))/(v1+np.sqrt(v1 ** 2+2*9.8*dy))
         except ZeroDivisionError:
             time += 1000
         v1 = np.sqrt(v1 ** 2+2*9.8*dy)
     return time

def GA(population):
    times = np.array([fitness(i) for i in population])
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
                temp[j] = random.uniform(0,displayHeight-gapWidth*2)
        newpop.append(temp)
    return np.array(newpop)
  

def DE(population):
    global N, DElmda, F, CR
    for i in range(DElmda):
        sample = list(range(DElmda))
        sample.remove(i)
        abc = random.sample(sample, 3)
        mutant = population[abc[0]] + F * (population[abc[1]]-population[abc[2]])
        np.clip(mutant, 0, displayHeight-gapWidth*2)
        for j in range(N):
            r = random.uniform(0,1)
            if r > CR:
                mutant[j] = population[i][j]
        if fitness(mutant) < fitness(population[i]):
            population[i] = mutant
    return population

def draw(alg, population):
    colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]
    if alg == "GA":
        x, y = gapWidth, gapWidth
        pygame.draw.lines(disp, THECOLORS[colours[0]], False, [(x+(displayWidth/3-gapWidth*2)/N*i, y+(displayHeight-gapWidth/2-p)) for i,p in enumerate(population[0])], 5)
    elif alg == "DE":
        x, y = displayWidth/3+gapWidth, gapWidth
    elif alg == "CMAES":
        x, y = 2*displayWidth/3+gapWidth, gapWidth
    for i in range(np.shape(population)[0]):
        pygame.draw.lines(disp, THECOLORS[colours[i%8]], False, [(x+(displayWidth/3-gapWidth*2)/N*i, y+(displayHeight-gapWidth/2-p)) for i,p in enumerate(population[i])])

def disptext(text, x, y):
    t = font.render(text, True, black)
    tRect = t.get_rect()
    tRect.center = (x/2,y/2)
    disp.blit(t,tRect)

pygame.init()
pygame.display.set_caption("Brachistochrone")
displayWidth = 1300
displayHeight = 600
gapWidth = 25
disp = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
running = True
white = (255,255,255)
black = (0,0,0)
font = pygame.font.Font("freesansbold.ttf", 32)


GApop = np.random.uniform(0,displayHeight-gapWidth*2, (GAlmda,N))
GApop[:,0] = displayHeight-gapWidth*2
GApop[:,-1] = gapWidth*2
DEpop = GApop[:DElmda,:]
es = cma.CMAEvolutionStrategy(DEpop[0], 0.5)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)

    disptext("Genetic Algorithm", displayWidth/3,gapWidth*1.5)
    disptext("Differential Evolution", displayWidth,gapWidth*1.5)
    disptext("CMA-ES", 5*displayWidth/3,gapWidth*1.5)

    GApop = GA(GApop)
    draw("GA", GApop)
    DEpop = DE(DEpop)
    draw("DE", DEpop)
    CMAESpop = es.ask()
    draw("CMAES", CMAESpop)
    es.tell(CMAESpop, [fitness(x) for x in CMAESpop])
    
    minima = brachistochrone(displayWidth/3-gapWidth*2,displayHeight-gapWidth*4)[-1]
    disptext("% Accuracy: " + str(round((fitness(GApop[0])-minima)/minima*100,3)), displayWidth/3, displayHeight*2-gapWidth*2)
    disptext("% Accuracy: " + str(round((fitness(DEpop[0])-minima)/minima*100,3)), displayWidth, displayHeight*2-gapWidth*2)
    disptext("% Accuracy: " + str(round((fitness(CMAESpop[0])-minima)/minima*100,3)), 5*displayWidth/3, displayHeight*2-gapWidth*2)



    pygame.display.update()
