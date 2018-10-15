import math
import random as rn
import numpy as np
import testfuncs_semenkina
edge =  math.pi
data_size = 300
dim = 2
bounds = [(-edge,edge)]
#bounds =[tuple(testfuncs_semenkina.getbounds("I7",2)) for d in range(dim)]
variables = ["x"+str(i) for i in range(len(bounds))]

data= []
optim_func = testfuncs_semenkina.myfunc

def objective_function(func):
    mse = 0
    try:
        for var,y in data:
            mse += (y-func(var))**2/len(data)
    except:
        return float('inf')
    mse **= 0.5
    return mse

# for i in range(data_size):
#     var = {}
#     for j,bound in enumerate(bounds):
#         var["x"+str(j)]  = rn.random()*(bound[1]-bound[0])+bound[0]
#     lvar = [x for x in var.values()]
#     if len(lvar) ==1 :
#         lvar = lvar[0]
#     data.append([var,optim_func(lvar)])


