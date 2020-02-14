import sys, pygame, pymunk, pymunk.pygame_util, random, time, numpy, math
from pygame.locals import *
from pygame.color import *

#NB: pymunk to pygame co-ordinates: y*-1 +600

#Values to toggle
pointnum = 25
popnum = 25
F = 0.8 ## 0-2 #0.8 #0.25
CR = 0.9 ## 0-1 #0.9 #0.55

colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]


#Ensures each ball only collides with its respective line
def coll(arbiter, space, data):
    a, b = arbiter.shapes
    return a.pair_index == b.pair_index


#Determines 'fitness' of each line
def disp(screen, space, population):

    #Clear space
    for s in space.shapes[:]:
        space.remove(s)
        try:
            space.remove(s.body)
        except:
            pass

    #Make lines
    for i in range(popnum):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = 100, 500
        for j in range(pointnum-1):
            line = pymunk.Segment(body, (j*round(600/(pointnum-1)), population[i][j]-500), ((j+1)*round(600/(pointnum-1)), population[i][j+1]-500), 1)
            line.color = THECOLORS[colours[i%8]]
            line.collision_type = 1
            line.pair_index = i+1
            space.add(line)

def fitness(alist):
    time = 0
    v1 = 0
    for i in range(pointnum-1):
        dy = abs(alist[i+1]-alist[i])
        try:
            time += (2 * math.sqrt((500/pointnum) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2+2*9.8*dy))
        except ZeroDivisionError:
            time += math.inf
        v1 = math.sqrt(v1 ** 2+2*9.8*dy)
    return time

##def fitness(vector):
##    vector[0] = 500
##    vector[-1] = 100
##    t = 0
##    v1 = 0
##
##    for i in range(pointnum-1):
##        dy = vector[i+1]-vector[i]
##        if (v1**2 - 2*9.81*dy) < 0:
##            t = 100000
##            break
##        elif i == 0 and dy > 0:
##            t = 100000
##            break
##        d = math.sqrt((20/pointnum)**2 + dy**2)
##        if (2*d)*(-v1 + math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy) < 0:
##            t += (2*d)*(-v1 - math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy)
##        else:
##            t += (2*d)*(-v1 + math.sqrt(v1**2 - 2*9.81*dy))/(9.81*dy)
##        v1 = math.sqrt(v1**2 - 2*9.81*dy)
##
##    return t

def recombinate(population):
    for i in range(popnum):
        sample = list(range(popnum))
        sample.remove(i)
        abc = random.sample(sample, 3)
        mutant = population[abc[0]] + F * (population[abc[1]]-population[abc[2]])
        numpy.clip(mutant, 0, 500)
        for j in range(pointnum):
            r = random.uniform(0,1)
            if r > CR:
                mutant[j] = population[i][j]
        if fitness(mutant) < fitness(population[i]):
            population[i] = mutant
    return population

        
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Brachistochrone")
    clock = pygame.time.Clock()

    #Initial seeded + random population
    population = numpy.zeros([popnum, pointnum])
    for i in range(popnum):
        population[i][0] = 500
        for j in range(pointnum-2):
            population[i][j + 1] = random.uniform(0,600)
        population[i][pointnum-1] = 100
    space = pymunk.Space()
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    disp(screen, space, population)
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
        for i in range(1):
            population = recombinate(population)
        disp(screen, space, population)
        
        space.step(1/500.0)
        space.step(1/500.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(200)

main()

