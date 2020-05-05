#Modified from https://github.com/andyfaff/ampgo

from __future__ import print_function

import numpy

OPENOPT = SCIPY = True

try:
    from openopt import NLP
except ImportError:
    OPENOPT = False
OPENOPT = False

try:
    from scipy.optimize import minimize
except ImportError:
    SCIPY = False

SCIPY_LOCAL_SOLVERS   = ['Nelder-Mead', 'Powell', 'L-BFGS-B', 'TNC', 'SLSQP']
OPENOPT_LOCAL_SOLVERS = ['bobyqa', 'ptn', 'slmvm2', 'ralg', 'mma', 'auglag', 'sqlcp']

tabuerror = False
succ = False
nfesuccess = numpy.inf
def AMPGO(objfun, x0, args=(), local='L-BFGS-B', local_opts=None, bounds=None, maxfunevals=None,
          totaliter=20, maxiter=5, glbtol=1e-5, eps1=0.02, eps2=0.1, tabulistsize=5,
          tabustrategy='farthest', fmin=-numpy.inf, disp=None):
    global tabuerror, succ, nfesuccess

    tabuerror = False
    succ = False
    nfesuccess = numpy.inf
    """
    Finds the global minimum of a function using the AMPGO (Adaptive Memory Programming for
    Global Optimization) algorithm. 
    
    :param `objfun`: Function to be optimized, in the form ``f(x, *args)``.
    :type `objfun`: callable
    :param `args`: Additional arguments passed to `objfun`.
    :type `args`: tuple
    :param `local`: The local minimization method (e.g. ``"L-BFGS-B"``). It can be one of the available
     `scipy` local solvers or `OpenOpt` solvers.
    :type `local`: string
    :param `bounds`: A list of tuples specifying the lower and upper bound for each independent variable
     [(`xl0`, `xu0`), (`xl1`, `xu1`), ...]
    :type `bounds`: list
    :param `maxfunevals`: The maximum number of function evaluations allowed.
    :type `maxfunevals`: integer
    :param `totaliter`: The maximum number of global iterations allowed.
    :type `totaliter`: integer
    :param `maxiter`: The maximum number of `Tabu Tunnelling` iterations allowed during each global iteration.
    :type `maxiter`: integer
    :param `glbtol`: The optimization will stop if the absolute difference between the current minimum objective
     function value and the provided global optimum (`fmin`) is less than `glbtol`.
    :type `glbtol`: float
    :param `eps1`: A constant used to define an aspiration value for the objective function during the Tunnelling phase.
    :type `eps1`: float
    :param `eps2`: Perturbation factor used to move away from the latest local minimum at the start of a Tunnelling phase.
    :type `eps2`: float
    :param `tabulistsize`: The size of the tabu search list (a circular list).
    :type `tabulistsize`: integer
    :param `tabustrategy`: The strategy to use when the size of the tabu list exceeds `tabulistsize`. It can be
     'oldest' to drop the oldest point from the tabu list or 'farthest' to drop the element farthest from
     the last local minimum found.
    :type `tabustrategy`: string
    :param `fmin`: If known, the objective function global optimum value.
    :type `fmin`: float
    :param `disp`: If zero or defaulted, then no output is printed on screen. If a positive number, then status
     messages are printed.
    :type `disp`: integer
 
    :returns: A tuple of 5 elements, in the following order:

     1. **best_x** (`array_like`): the estimated position of the global minimum.
     2. **best_f** (`float`): the value of `objfun` at the minimum.
     3. **evaluations** (`integer`): the number of function evaluations.
     4. **msg** (`string`): a message describes the cause of the termination.
     5. **tunnel_info** (`tuple`): a tuple containing the total number of Tunnelling phases performed and the
        successful ones.

    :rtype: `tuple`

    The detailed implementation of AMPGO is described in the paper 
    "Adaptive Memory Programming for Constrained Global Optimization" located here:

    http://leeds-faculty.colorado.edu/glover/fred%20pubs/416%20-%20AMP%20(TS)%20for%20Constrained%20Global%20Opt%20w%20Lasdon%20et%20al%20.pdf

    Copyright 2014 Andrea Gavana
    """
   
    if local not in SCIPY_LOCAL_SOLVERS + OPENOPT_LOCAL_SOLVERS:
        raise Exception('Invalid local solver selected: %s'%local)

    if local in SCIPY_LOCAL_SOLVERS and not SCIPY:
        raise Exception('The selected solver %s is not available as there is no scipy installation'%local)

    if local in OPENOPT_LOCAL_SOLVERS and not OPENOPT:
        raise Exception('The selected solver %s is not available as there is no OpenOpt installation'%local)
        
    x0 = numpy.atleast_1d(x0)
    n = len(x0)

    if bounds is None:
        bounds = [(None, None)] * n
##    if len(bounds) != n:
##        raise ValueError('length of x0 != length of bounds')

    low = [0]*n
    up = [0]*n
    
    for i in range(n):
        if bounds[i] is None:
            l, u = -numpy.inf, numpy.inf
        else:
            l, u = bounds[i]
            if l is None:
                low[i] = -numpy.inf
            else:
                low[i] = l
            if u is None:
                up[i] = numpy.inf
            else:
                up[i] = u

    if maxfunevals is None:
        maxfunevals = max(100, 10*len(x0))

    if tabulistsize < 1:
        raise Exception('Invalid tabulistsize specified: %s. It should be an integer greater than zero.'%tabulistsize)
    if tabustrategy not in ['oldest', 'farthest']:
        raise Exception('Invalid tabustrategy specified: %s. It must be one of "oldest" or "farthest"'%tabustrategy)

    iprint = 50
    if disp is None or disp <= 0:
        disp = 0
        iprint = -1

    low = numpy.asarray(low)
    up = numpy.asarray(up)

    tabulist = []
    best_f = numpy.inf
    best_x = x0
    
    global_iter = 0
    all_tunnel = success_tunnel = 0
    evaluations = 0

    if glbtol < 1e-8:
        local_tol = glbtol
    else:
        local_tol = 1e-8

    while 1:

        if disp > 0:
            print('\n')
            print('='*72)
            print('Starting MINIMIZATION Phase %-3d'%(global_iter+1))
            print('='*72)

        if local in OPENOPT_LOCAL_SOLVERS:
            problem = NLP(objfun, x0, lb=low, ub=up, maxFunEvals=max(1, maxfunevals), ftol=local_tol, iprint=iprint)
            problem.args = args
            
            results = problem.solve(local)
            xf, yf, num_fun = results.xf, results.ff, results.evals['f']
        else:
            options = {'maxiter': max(1, maxfunevals), 'disp': disp}
            if local_opts is not None:
                options.update(local_opts)
            res = minimize(objfun, x0, args=args, method=local, bounds=bounds, tol=local_tol, options=options)
            xf, yf, num_fun = res['x'], res['fun'], res['nfev']
        
        maxfunevals -= num_fun
        evaluations += num_fun

        if yf < best_f:
            best_f = yf
            best_x = xf

        if disp > 0:
            print('\n\n ==> Reached local minimum: %s\n'%yf)
        
        # if best_f < fmin + glbtol:
        #     if disp > 0:
        #         print('='*72)
        #     return best_x, best_f, evaluations, 'Optimization terminated successfully', (all_tunnel, success_tunnel)
        if maxfunevals <= 0:
            if disp > 0:
                print('='*72)
            return best_x, best_f, evaluations, 'Maximum number of function evaluations exceeded', (all_tunnel, success_tunnel)

        tabulist = drop_tabu_points(xf, tabulist, tabulistsize, tabustrategy)
        tabulist.append(xf)

        i = improve = 0

        while i < maxiter and improve == 0:

            if disp > 0:
                print('-'*72)
                print('Starting TUNNELLING   Phase (%3d-%3d)'%(global_iter+1, i+1))
                print('-'*72)

            all_tunnel += 1
            
            r = numpy.random.uniform(-1.0, 1.0, size=(n, ))
            beta = eps2*numpy.linalg.norm(xf)/numpy.linalg.norm(r)
            
            if numpy.abs(beta) < 1e-8:
                beta = eps2
                
            x0  = xf + beta*r

            x0 = numpy.where(x0 < low, low, x0)
            x0 = numpy.where(x0 > up , up , x0)

            aspiration = best_f - eps1*(1.0 + numpy.abs(best_f))

            tunnel_args = tuple([objfun, aspiration, tabulist] + list(args))

            if local in OPENOPT_LOCAL_SOLVERS:
                problem = NLP(tunnel, x0, lb=low, ub=up, maxFunEvals=max(1, maxfunevals), ftol=local_tol, iprint=iprint)
                problem.args = tunnel_args
                
                results = problem.solve(local)
                xf, yf, num_fun = results.xf, results.ff, results.evals['f']
            else:
                options = {'maxiter': max(1, maxfunevals), 'disp': disp}
                if local_opts is not None:
                    options.update(local_opts)

                res = minimize(tunnel, x0, args=tunnel_args, method=local, bounds=bounds, tol=local_tol, options=options)
                xf, yf, num_fun = res['x'], res['fun'], res['nfev']

            maxfunevals -= num_fun
            evaluations += num_fun

            yf = inverse_tunnel(xf, yf, aspiration, tabulist)

            if yf <= best_f + glbtol:
                oldf = best_f
                best_f = yf
                best_x = xf
                improve = 1
                success_tunnel += 1

                if disp > 0:
                    print('\n\n ==> Successful tunnelling phase. Reached local minimum: %s < %s\n'%(yf, oldf))

            # if best_f < fmin + glbtol:
            #     return best_x, best_f, evaluations, 'Optimization terminated successfully', (all_tunnel, success_tunnel)

            i += 1
                        
            if maxfunevals <= 0:
                return best_x, best_f, evaluations, 'Maximum number of global iterations exceeded', (all_tunnel, success_tunnel), nfesuccess, succ

            tabulist = drop_tabu_points(xf, tabulist, tabulistsize, tabustrategy)
            tabulist.append(xf)

            if best_f-fmin < 1e-3 and succ == False:
                succ = True
                nfesuccess = evaluations

            if tabuerror:
                break
            

        if disp > 0:
            print('='*72)

        global_iter += 1
        x0 = xf.copy()

        if global_iter >= totaliter:
            return best_x, best_f, evaluations, 'Maximum number of global iterations exceeded', (all_tunnel, success_tunnel), nfesuccess, succ

        # if best_f < fmin + glbtol:
        #     return best_x, best_f, evaluations, 'Optimization terminated successfully', (all_tunnel, success_tunnel)


def drop_tabu_points(xf, tabulist, tabulistsize, tabustrategy):

    if len(tabulist) < tabulistsize:
        return tabulist
    
    if tabustrategy == 'oldest':
        tabulist.pop(0)
    else:
        distance = numpy.sqrt(numpy.sum((tabulist-xf)**2, axis=1))
        index = numpy.argmax(distance)
        tabulist.pop(index)

    return tabulist


def tunnel(x0, *args):
    global tabuerror, succ

    objfun, aspiration, tabulist = args[0:3]

    fun_args = ()    
    if len(args) > 3:
        fun_args = tuple(args[3:])

    numerator = (objfun(x0, *fun_args) - aspiration)**2
    denominator = 1.0


    for tabu in tabulist:
        if numpy.sum((x0 - tabu)**2) == 0:
            tabuerror = True
            break
        denominator = denominator*numpy.sqrt(numpy.sum((x0 - tabu)**2))

    if not tabuerror:
        ytf = numerator/denominator
        return ytf
    else:
        return numpy.inf


def inverse_tunnel(xtf, ytf, aspiration, tabulist):

    denominator = 1.0

    for tabu in tabulist:
        denominator = denominator*numpy.sqrt(numpy.sum((xtf - tabu)**2))

    numerator = ytf*denominator
    
    yf = aspiration + numpy.sqrt(ytf*denominator)
    return yf



def sphere(x):
    return numpy.sum(x**2)

def bartelsconn(x):
    return abs(x[0]**2 + x[1]**2 + x[0]*x[1]) + abs(numpy.sin(x[0])) + abs(numpy.cos(x[1]))

def dropwave(x):
    return -(1 + numpy.cos(12 * numpy.sqrt(x[0]**2 + x[1]**2))) / (0.5 * (x[0]**2 + x[1]**2) + 2)

def easom(x):
    return -numpy.cos(x[0])*numpy.cos(x[1]) * numpy.exp(-(x[0]-numpy.pi)**2 -(x[1]-numpy.pi)**2)

def rotatedhe(x):
    return sum([(numpy.shape(x)[0]-j)*k for j,k in enumerate(x**2)])

def ackley(x):
    return -20 * numpy.exp( -0.2* numpy.sqrt( numpy.sum(x**2)/numpy.shape(x)[0] )) - numpy.exp( numpy.sum( numpy.cos(2*numpy.pi*x)) / numpy.shape(x)[0] ) + 20 + numpy.exp(1)

def schwefel(x):
    return 418.982887272433799807913601398*numpy.shape(x)[0] - numpy.sum(x*numpy.sin(numpy.sqrt(numpy.abs(x))))

def rastrigin(x):
    return 10*numpy.shape(x)[0] + numpy.sum(x**2 - 10*numpy.cos(2*numpy.pi*x))

def rosenbrock(x):
    return numpy.sum(100*(x[1:]-x[:-1]**2)**2 + (1-x[:-1])**2)

def zakharov(x):
    return numpy.sum(x**2) + numpy.sum(0.5 * x * numpy.arange(1,numpy.shape(x)[0]+1))**2 + numpy.sum(0.5 * x * numpy.arange(1,numpy.shape(x)[0]+1))**4

def michalewicz(x):
    return -numpy.sum( numpy.sin(x) * numpy.sin( (numpy.arange(1,numpy.shape(x)[0]+1) * (x**2)) / numpy.pi ) ** (2*10) )

def step(x):
    return numpy.sum(numpy.floor(numpy.abs(x)))


bounds = {
    "sphere": [-5.12,5.12],
    "bartelsconn": [-500,500],
    "dropwave": [-5.12,5.12],
    "easom": [-100,100],
    "rotatedhe": [-65.536, 65.536],
    "ackley": [-32.768, 32.768],
    "schwefel": [-500,500],
    "rastrigin": [-5.12,5.12],
    "rosenbrock": [-5,10],
    "zakharov": [-5,10],
    "michalewicz": [0, numpy.pi],
    "step": [-100,100]
    }
minima = {
    "sphere": 0,
    "bartelsconn": 1,
    "dropwave": -1,
    "easom": -1,
    "michalewicz": -4.6876581791, #	-1.8013034101, -4.6876581791, -9.6601517156
    "schwefel": 0,
    "rastrigin": 0,
    "rosenbrock": 0,
    "sphere10": 0,
    "rotatedhe": 0,
    "ackley": 0,
    "zakharov": 0,
    "step": 0
    }

def test(fobj, fobjstr, n):
    results = []
    for i in range(5):
        x0 = numpy.random.uniform(bounds[fobjstr][0],bounds[fobjstr][1],(n,1))
        bound = [(bounds[fobjstr][0],bounds[fobjstr][1]) for i in range(n)]
        xf, yf, fun_evals, msg, tt,nfesuccess,succ = AMPGO(fobj, x0, (), "L-BFGS-B", None, bound, 10000, 1000, 5, 1e-5, 0.02, 0.01 ,5, 'oldest', minima[fobjstr], None)
        results.append([nfesuccess, succ, x0, yf])
    return results

def bhtestset():
    data = []
    data.append(test(sphere, "sphere", 2))
    data.append(test(bartelsconn, "bartelsconn", 2))
    data.append(test(dropwave, "dropwave", 2))
    data.append(test(easom, "easom", 2))
    data.appendtest(michalewicz, "michalewicz", 5))
    data.append(test(schwefel, "schwefel", 5))
    data.append(test(rastrigin, "rastrigin", 5))
    data.append(test(rosenbrock, "rosenbrock", 5))
    data.append(test(sphere, "sphere", 10))
    data.append(test(rotatedhe, "rotatedhe", 10))
    data.append(test(ackley, "ackley", 10))
    data.append(test(zakharov, "zakharov", 10))
    data.append(test(step, "step", 10))
    pickle.dump(data, open( "ampgo.p", "wb" ))