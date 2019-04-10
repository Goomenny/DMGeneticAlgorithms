
import random as rn
import testfuncs_semenkina

class problem():
    def __init__(self, obj_func,dim):
        self.obj_func = obj_func
        self.__name__ = obj_func.__name__
        self.data_size = 300
        self.data = []
        self.dim = dim
        self.bounds =[tuple(testfuncs_semenkina.getbounds(self.__name__,dim))]
        self.variables = ["x" + str(i) for i in range(len(self.bounds))]
        for i in range(self.data_size):
            var = {}
            for j, bound in enumerate(self.bounds):
                var["x" + str(j)] = rn.random() * (bound[1] - bound[0]) + bound[0]
            lvar = [x for x in var.values()]
            if len(lvar) == 1:
                lvar = lvar[0]
            self.data.append([var, self.obj_func(lvar)])

    def __str__(self):
        return self.__name__
    def __call__(self, yy):
        mse = 0
        try:
            for var, y in self.data:
                mse += (y - yy(var)) ** 2 / len(self.data)
        except:
            return float('inf')
        mse **= 0.5
        return mse

# def objective_function(func):
#     mse = 0
#     try:
#         for var,y in data:
#             mse += (y-func(var))**2/len(data)
#     except:
#         return float('inf')
#     mse **= 0.5
#     return mse




