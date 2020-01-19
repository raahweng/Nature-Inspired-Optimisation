import sys, pygame, pymunk, pymunk.pygame_util, random, time
from pygame.locals import *
from pygame.color import *
from decimal import Decimal, ROUND_HALF_EVEN

#NB: pymunk to pygame co-ordinates: y*-1 +600
#NB Dont use mutations on starting points!

colours = ["red", "orange", "yellow", "green", "blue", "purple"]
times = [-1, -1, -1, -1, -1, -1, -1]
start = 0

#Ensures each ball only collides with its respective line
def coll(arbiter, space, data):
    a, b = arbiter.shapes
    return a.pair_index == b.pair_index

#Calculates how much time it takes for the ball to get from A to B
def get_time(arbiter, space, data):
    global start
    obj = arbiter.shapes[0]
    times[int(obj.pair_index)-1] = Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN)-start
    return True

def fitness(screen, space, population):
    global start
    start = Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN)

    #Make ball
    for i in range(6):
        moment = pymunk.moment_for_circle(1, 0, 1)
        body = pymunk.Body(100, moment)
        body.position = 101, 500  
        ball = pymunk.Circle(body, 5)
        ball.color = THECOLORS[colours[i]]
        ball.elasticity = 1.0
        ball.collision_type = 1
        ball.pair_index = i+1
        space.add(body, ball) 
        
    #Make lines
    for i in range(6):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = 100, 500
        for j in range(99):
            line = pymunk.Segment(body, (j*6, population[i][j]-500), (j*6+6, population[i][j+1]-500), 1)
            line.color = THECOLORS[colours[i]]
            line.collision_type = 1
            line.pair_index = i+1
            space.add(line)

    #Make sensors
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = 700, 100  
    sensor = pymunk.Circle(body, 6)
    sensor.sensor = True
    sensor.color = THECOLORS["grey"]
    sensor.collision_type = 2
    space.add(body, sensor)

    #Make collision handlers
    collision = space.add_collision_handler(1,1)
    collision.begin = coll
    time_handler = space.add_collision_handler(1,2)
    time_handler.begin = get_time

    

def main():
    global start
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Brachistochrone")
    clock = pygame.time.Clock()

    #Initial random population
    population = []
    points = []
    for j in range(2):
        for i in range(99):
            points.append(-4*(i)+ 500)
        points.append(100)
        population.append(points)
    for i in range(4):
        points = []
        points.append(500)
        for j in range(98): 
            points.append(random.randint(0,600))
        points.append(100)
        population.append(points)
    space = pymunk.Space()
    space.gravity = (0.0, -10000.0)
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    fitness(screen, space, population)
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        if Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN) > start+10:
            print(times)
            
        space.step(1/500.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(200)

if __name__ == '__main__':
    main()

