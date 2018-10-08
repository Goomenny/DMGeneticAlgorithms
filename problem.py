import math
import random as rn
import numpy as np
from scipy.optimize import rosen
edge =  math.pi
data_size = 300
bounds = [(-edge,edge),(-edge,edge)]
variables = ["x"+str(i) for i in range(len(bounds))]

data= []


def objective_function(func):
    mse = 0

    for var,y in data:
        mse += (y-func(var))**2

    mse = (mse/len(data)) ** 0.5
    return mse

for i in range(data_size):
    var = {}
    for j,bound in enumerate(bounds):
        var["x"+str(j)]  = rn.random()*(bound[1]-bound[0])+bound[0]
    data.append([var,optim_func(var)])


