import sys, random, time, cma, importlib
import numpy as np

bounds = {
    "sphere": [-5.12,5.12],
    "bartelsconn": [500,500],
    "dropwave": [-5.12,5.12],
    "easom": [-100,100],
    "rotatedhe": [-65.536, 65.536],
    "ackley": [-32.768, 32.768],
    "schwefel": [-500,500],
    "rastrigin": [-5.12,5.12],
    "rosenbrock": [-5,10],
    "zakharov": [-5,10],
    "michalewicz": [0, np.pi,
    "step": [-100,100]
    }


def sphere(x):
    return np.sum(x**2)

def bartelsconn(x):
    return abs(x[0]**2 + x[1]**2 + x[0]*x[1]) + abs(np.sin(x[0])) + abs(np.cos(x[1]))

def dropwave(x):
    return -(1 + np.cos(12 * np.sqrt(x[0]**2 + x[1]**2))) / (0.5 * (x[0]**2 + x[1]**2) + 2)

def easom(x):
    return -np.cos(x[0])*np.cos(x[1]) * np.exp(-(x[0]-np.pi)**2 -(x[1]-np.pi)**2)

def rotatedhe(x):
    return sum([(np.shape(x)[0]-j)*k for j,k in enumerate(x**2)])

def ackley(x):
    return -20 * np.exp( -0.2* np.sqrt( np.sum(x**2)/np.shape(x)[0] )) - np.exp( np.sum( np.cos(2*np.pi*x)) / np.shape(x)[0] ) + 20 + np.exp(1)

def schwefel(x):
    return 418.982887272433799807913601398*np.shape(x)[0] - np.sum(x*np.sin(np.sqrt(np.abs(x))))

def rastrigin(x):
    return 10*np.shape(x)[0] + np.sum(x**2 - 10*np.cos(2*np.pi*x))

def rosenbrock(x):
    return np.sum(100*(x[1:]-x[:-1]**2)**2 + (1-x[:-1])**2)

def zakharov(x):
    return np.sum(x**2) + np.sum(0.5 * x * np.arange(1,np.shape(x)[0]+1))**2 + np.sum(0.5 * x * np.arange(1,np.shape(x)[0]+1))**4

def michalewicz(x):
    return - np.sum(np.sin(x) * np.sin( np.arange(1,np.shape(x)[0]+1) * x**2 / np.pi ) ** 2*10)

def step(x):
    return np.sum(np.floor(np.abs(x)))