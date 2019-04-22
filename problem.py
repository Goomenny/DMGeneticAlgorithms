import numpy as np
import random as rn
import testfuncs_semenkina

class problem():
    def __init__(self, obj_func,dim):
        self.obj_func = obj_func
        self.__name__ = obj_func.__name__
        self.data_size = 800
        self.data = []
        self.dim = dim
        self.bounds =[tuple(testfuncs_semenkina.getbounds(self.__name__,d)) for d in range(dim)]
        self.variables = ["x" + str(i) for i in range(len(self.bounds))]
        self.np_var = []
        self.np_y = []
        for i in range(self.data_size):
            var = {}
            for j, bound in enumerate(self.bounds):
                var["x" + str(j)] = rn.random() * (bound[1] - bound[0]) + bound[0]
            lvar = [x for x in var.values()]
            self.np_var.append(lvar)
            if len(lvar) == 1:
                lvar = lvar[0]
            self.data.append([var, self.obj_func(lvar)])
            self.np_y.append(self.obj_func(lvar))
        self.np_var = np.array(self.np_var)
        self.np_y = np.array(self.np_y)
    def __str__(self):
        return self.__name__
    def __call__(self, yy):
        mse = self.np_y-yy(self.np_var)
        variation = self.np_y.max()-self.np_y.min()
        mse **= 2
        mse=mse.mean()
        # mse = 0
        # try:
        #     for var, y in self.data:
        #         mse += (y - yy(var)) ** 2 / len(self.data)
        # except:
        #     return float('inf')
        mse **= 0.5
        return mse/variation

# def objective_function(func):
#     mse = 0
#     try:
#         for var,y in data:
#             mse += (y-func(var))**2/len(data)
#     except:
#         return float('inf')
#     mse **= 0.5
#     return mse




