import numpy as np
import testfuncs_semenkina

class problem():
    def __init__(self, obj_func,dim):
        self.obj_func = obj_func
        self.__name__ = obj_func.__name__
        self.data_size = 800

        self.dim = dim
        self.bounds =[tuple(testfuncs_semenkina.getbounds(self.__name__,d)) for d in range(dim)]
        self.variables = ["x" + str(i) for i in range(len(self.bounds))]

        self.np_y = np.zeros(self.data_size)
        self.np_var = np.random.sample((self.data_size, dim))

        for i in range(dim):
            self.np_var[:,i] = self.np_var[:,i]* (self.bounds[i][1] - self.bounds[i][0]) + self.bounds[i][0]

        for i in range(self.data_size):
            self.np_y[i] = self.obj_func(self.np_var[i])
        self.variation = self.np_y.max() - self.np_y.min()
    def __str__(self):
        return self.__name__
    def __call__(self, yy):

        mse = self.np_y-yy(self.np_var)
        mse = mse/self.data_size**0.5

        mse **= 2
        mse = mse.sum()
        mse **= 0.5

        return mse/self.variation




