import sys, pygame, pymunk, pymunk.pygame_util, random, time
from pygame.locals import *
from pygame.color import *
from decimal import Decimal, ROUND_HALF_EVEN

#NB: pymunk to pygame co-ordinates: y*-1 +600
#NB Dont use mutations on starting points!

#Values to toggle
pop = 6
pointnum = 100

colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]
times = []
start = 0

#Ensures each ball only collides with its respective line
def coll(arbiter, space, data):
    a, b = arbiter.shapes
    return a.pair_index == b.pair_index

#Determines 'fitness' of each line
def fitness(screen, space, population):
    global start
    start = Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN)
    #Clear space
    for s in space.shapes[:]:
        space.remove(s)
        try:
            space.remove(s.body)
        except:
            pass

    #Make ball
    for i in range(pop):
        moment = pymunk.moment_for_circle(1, 0, 1)
        body = pymunk.Body(100, moment)
        body.position = 101, 500  
        ball = pymunk.Circle(body, 5)
        ball.color = THECOLORS[colours[i%8]]
        ball.elasticity = 1.0
        ball.collision_type = 1
        ball.pair_index = i+1
        space.add(body, ball) 
        
    #Make lines
    for i in range(pop):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = 100, 500
        for j in range(pointnum-1):
            line = pymunk.Segment(body, (j*round(600/(pointnum-1)), population[i][j]-500), ((j+1)*round(600/(pointnum-1)), population[i][j+1]-500), 1)
            line.color = THECOLORS[colours[i%8]]
            line.collision_type = 1
            line.pair_index = i+1
            space.add(line)

    #Make sensors
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = 700, 100  
    sensor = pymunk.Circle(body, 7)
    sensor.sensor = True
    sensor.color = THECOLORS["grey"]
    sensor.collision_type = 2
    space.add(body, sensor)

    #Make collision handlers
    collision = space.add_collision_handler(1,1)
    collision.begin = coll
                        
        
def main():
    global start
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Brachistochrone")
    clock = pygame.time.Clock()

    #Initial seeded + random population
    population = []
    points = []
    for j in range(pop):
        for i in range(99):
            points.append(-4*(i)+ 500)
        points.append(100)
        population.append(points)
##    for i in range(0):
##        points = []
##        points.append(500)
##        for j in range(98): 
##            points.append(random.randint(0,600))
##        points.append(100)
##        population.append(points)
    space = pymunk.Space()
    space.gravity = (0.0, -100000.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    fitness(screen, space, population)
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_r:
                fitness(screen, space, population)
                step = input("step")
        step = 0.002

##        if Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN) > start+100:
##            for s in space.shapes[:]:
##                space.remove(s)
##                try:
##                    space.remove(s.body)
##                except:
##                    pass
##            fitness(screen, space, population)
        
        space.step(step)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(200)


if __name__ == '__main__':
    main()

