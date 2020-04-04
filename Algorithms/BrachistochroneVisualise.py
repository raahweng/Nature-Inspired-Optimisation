import sys, pygame, random, time, cma, importlib
from scipy.optimize import newton
import numpy as np
from pygame.color import *

inp = input("Enter Algorithm ")
alg = importlib.import_module(inp)

#Pygame variables
pygame.init()
displayWidth = 800
displayHeight = 800
gapWidth = 40
disp = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
running = True
white = (255,255,255)
black = (0,0,0)
font = pygame.font.Font("freesansbold.ttf", 32)
counter = -1
ite = 0

N = 25
startend = (displayHeight-gapWidth*2,gapWidth*8)
bounds = (displayHeight-gapWidth*2,0)

#Calculates time of descent for slope generated; Uses Conservation of Energy and Diff/Int w.r.t
def fitness(vector):
    vector[0] = startend[0]
    vector[-1] = startend[1]
    dx = (displayWidth-gapWidth*2)/(N-1)
    t=0
    for i in range(N-1):
        d = np.sqrt(dx**2 + (vector[i]-vector[i+1])**2)
        a,b = vector[0]-vector[i+1], vector[0]-vector[i]
        if a >= 0 and b >= 0:
            t += d*( np.sqrt(a) - np.sqrt(b))/(vector[i]-vector[i+1])

        #Penalise if impossible to slide uphill by number of illegal points
        else:
            t += (np.sum(a < 0, axis=0) + np.sum(b < 0, axis=0))*100
    t *= np.sqrt(2/9.81)
    return t

#Calculates equation and time of descent for a Brachistochrone
def brachistochrone(x2,y2):
    #Calculate theta2 using Newton-Raphson numerical method + Parametric equation of cycloid
    def f(theta):
        return y2/x2 - (1-np.cos(theta))/(theta-np.sin(theta))
    theta2 = newton(f, np.pi/2)
    R = y2 / (1 - np.cos(theta2))
    theta = np.linspace(0, theta2, 100)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))
    T = theta2 * np.sqrt(R / 9.8)
    return x, y, T

#Find fitness of fittest individual
def fittest(population):
    if np.shape(population)[1] > 1:
        return min([fitness(i) for i in population])
    else:
        return min(fitness(population))

#Draw population
def draw(population, ite):
    colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]
    x, y = gapWidth, gapWidth
    if alg.name() == "Simulated Annealing":
        pygame.draw.lines(disp, THECOLORS[colours[0]], False, [(int((x+(displayWidth-gapWidth*2)/N*i)), int(y+(displayHeight-gapWidth/2-p))) for i,p in enumerate(population)], 3)
    else:
        for i in range(np.shape(population)[0]):
            pygame.draw.lines(disp, THECOLORS[colours[i%8]], False, [(int((x+(displayWidth-gapWidth*2)/N*i)), int(y+(displayHeight-gapWidth/2-p))) for i,p in enumerate(population[i])])
        if alg.name() == "Genetic Algorithm":
            pygame.draw.lines(disp, THECOLORS[colours[0]], False, [(int((x+(displayWidth-gapWidth*2)/N*i)), int(y+(displayHeight-gapWidth/2-p))) for i,p in enumerate(population[0])], 5)


#Render text
def disptext(text, x, y):
    t = font.render(text, True, black)
    tRect = t.get_rect()
    tRect.center = (int(x/2),int(y/2))
    disp.blit(t,tRect)

#Main display loop
while running:
    ite += 1
    maxite = 500

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)

    pygame.display.set_caption("Brachistochrone Generation " + str(counter % maxite))
    counter += 1

    #Each test lasts maxite generations before restarting and randomly reinitialising the population
    if counter % maxite ==0:

        ite = 0
        #Uniformly random initialisation of population with fixed start/end point; each algorithm starts with the same population clipped to their respective population size
        population = alg.initialise(bounds, N, fitness, maxite)
        if alg.name() == "Simulated Annealing":
            population[0][0], population[-1][0] = startend[0],startend[1]
        elif alg.name == "CMA-ES":
            population[0] = startend[0]
            population[-1] = startend[1]
        else:
            population[:,0] = startend[0]
            population[:,-1] = startend[1]
    
    #Iterative recombination of population
    population = alg.f(population, fitness, bounds, N, ite, maxite)

    #GUI stuff
    disptext(alg.name(), displayWidth,gapWidth*1.5)
    draw(population, ite)

    #Percentage accuracy off Global Minima; Evaluates fittest individual after 300 generations
    minima = brachistochrone(displayWidth-gapWidth*2,startend[0]-startend[1])[-1]
    disptext("% Error: " + str(round((fittest(population)-minima)/minima*100,3)), displayWidth, displayHeight*2-gapWidth*2)

    pygame.display.update()
