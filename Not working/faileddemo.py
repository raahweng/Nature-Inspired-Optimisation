import sys, pygame, pymunk, pymunk.pygame_util, random, time
from pygame.locals import *
from pygame.color import *
from decimal import Decimal, ROUND_HALF_EVEN

#NB: pymunk to pygame co-ordinates: y*-1 +600
#NB Dont use mutations on starting points!

#Values to toggle
popnum = 10
pointnum = 10

colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "grey"]
times = []
for i in range(popnum):
    times.append([Decimal('100'),i])
start = 0
closest = ()


#Ensures each ball only collides with its respective line
def coll(arbiter, space, data):
    a, b = arbiter.shapes
    return a.pair_index == b.pair_index


#Calculates how much time it takes for the ball to get from A to B
def get_time(arbiter, space, data):
    global start
    obj = arbiter.shapes[0]
    times[int(obj.pair_index)-1][0] = Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN)-start
    return True


#Determines 'fitness' of each line
def fitness(screen, space, population):
    global start
    times = []
    for i in range(popnum):
        times.append([Decimal('100'),i])
    start = Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN)

    #Clear space
    for s in space.shapes[:]:
        space.remove(s)
        try:
            space.remove(s.body)
        except:
            pass

    #Make balls
    for i in range(popnum):
        moment = pymunk.moment_for_circle(1, 0, 1)
        body = pymunk.Body(100, moment)
        body.position = 101, 500  
        ball = pymunk.Circle(body, 5)
        ball.color = THECOLORS[colours[i%8]]
        ball.elasticity = 1.0
        ball.collision_type = 1
        ball.pair_index = i+1
        ball.filter = pymunk.ShapeFilter(categories=0b0001)
        space.add(body, ball) 
        
    #Make lines
    for i in range(popnum):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = 100, 500
        for j in range(pointnum-1):
            line = pymunk.Segment(body, (j*round(600/(pointnum-1)), population[i][j]-500), ((j+1)*round(600/(pointnum-1)), population[i][j+1]-500), 1)
            line.color = THECOLORS[colours[i%8]]
            line.collision_type = 1
            line.pair_index = i+1
            line.filter = pymunk.ShapeFilter(categories=0b0010)
            space.add(line)

    #Make sensor
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = 700, 100  
    sensor = pymunk.Circle(body, 8)
    sensor.sensor = True
    sensor.color = THECOLORS["grey"]
    sensor.collision_type = 2
    space.add(body, sensor)

    #Make collision handlers
    collision = space.add_collision_handler(1,1)
    collision.begin = coll
    time_handler = space.add_collision_handler(1,2)
    time_handler.begin = get_time

    
#Crossover + Mutation to generate new, 'fitter' population
def gene_mix(population, times, close):
    global closest
    
    #Fitness defined by time taken to reach endpoint, number of balls that did not make endpoint are counted
    times.sort()
    order = []
    counter = 0
    for i in range(len(times)):
        if times[i][0] == Decimal('100'):
            counter += 1
        order.append(times[i][1])
        
    #If none reach the endpoint, then the closest ball is used as the 'fittest'
    if counter == popnum:
        print("failure")
        a = order.index(closest-1)
        order[a], order[0] = order[0], order[a]
    population = [population[i] for i in order] 
    new_pop = [[] for i in range(popnum)]

    #Elitism; the 'fittest' line automatically survives to the next generation
    new_pop[0] = population[0]

    #     
    for i in range(popnum):
        if new_pop[i] == []:
            new_pop[i].append(500)
            for j in range(pointnum-2):
                chance = random.uniform(1,pointnum)
                if chance >= pointnum - 0.5:
                    new_pop[i].append(random.randint(0,500))
                else:
                    upper = 0
                    lower = 0
                    for k in range(counter):
                        lower = upper
                        upper += (pointnum/(counter*(counter+1)/2))*(k+1)
                        if lower <= chance <= upper:
                            new_pop[i].append(population[counter-k][j+1])
            new_pop[i].append(100)
        if len(new_pop[i]) != pointnum:
            print(i)
    print(new_pop)
    return new_pop
                        
        
def main():
    global start
    global closest
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Brachistochrone")
    clock = pygame.time.Clock()
    

    #Initial seeded population (straight line) to speed up process
    population = []
    for j in range(3):
        points = []
        points.append(500)
        for i in range(pointnum-1):
            points.append((-400/(pointnum-1))*(i+1)+ 500)
        points.append(100)
        population.append(points)
    #Initial random population to explore values
    for i in range(popnum-3):
        points = []
        points.append(500)
        for j in range(pointnum-2): 
            points.append(random.randint(0,600))
        points.append(100)
        population.append(points)
    space = pymunk.Space()
    space.gravity = (0.0, -10000) #-50000.0
    draw_options = pymunk.pygame_util.DrawOptions(screen)


    fitness(screen, space, population)
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)

        if Decimal(time.time()).quantize(Decimal('.0000000001'), rounding=ROUND_HALF_EVEN) > start+Decimal(1.5):
            closest = space.point_query_nearest((700,100), 100, pymunk.ShapeFilter())[0].pair_index
            print("closest", colours[(closest-1)%8])
            for i in space.shapes[:]:
                space.remove(i)
                try:
                    space.remove(i.body)
                except:
                    pass
            fitness(screen, space, gene_mix(population, times, closest))
            
        for i in range(5):
            space.step(1/500.0)
        screen.fill((255,255,255))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(200)

main()


##Things to fix:
##    Extra items in list
##    Ball not touching sensor when it should: barrier?
##    Crossover for top 3 nearest
##    Elitism doesnt always work
##    Too slow
