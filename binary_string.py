import math
import random as rn
import copy
import numpy as np
class binary_string:
    def __init__(self,
                 bounds = None):
        self.accuracy = 0.001
        self.E = {}
        self.bounds = {}
        self.N = {}
        self.size = 0
        self.dec = {}
        for dim,bound in enumerate(bounds):
            N = math.log((bound[1]-bound[0])/(0.1*self.accuracy))/math.log(2)
            if int(N) != N:
                N = int(N+1)
            else:
                N = int(N)
            self.N["x"+str(dim)] =  (N,self.size+N) #np.array([rn.choice([0,1]) for i in range(N)])
            self.size += N
            self.E["x" + str(dim)] = (bound[1]-bound[0])/(2**N*0.1)
            self.bounds["x" + str(dim)] = [bound[0],bound[1]]
        self.cargo = np.array([rn.choice([0, 1]) for i in range(self.size)])
        self.fitness = None
        self.changed = True


    def __str__(self):
        return str(self.get_result())

    def copy(self,other):
        self.cargo = other.cargo.copy()
        self.fitness = other.fitness

    def calculate_result(self):
        for dim,n in self.N.items():
            summa = (self.cargo[n[1]-n[0]:n[1]] * 2 ** np.arange(n[0])).sum()
            self.dec[dim] = self.bounds[dim][0]+summa*self.E[dim]*0.1


    def get_result(self):
        self.calculate_result()
        return [x for x in self.dec.values()]

    def calculate_fitness(self, obj_func):

        self.fitness = 1 / (1 + obj_func(self.get_result))
        self.changed = False

    def mutate(self, mutation_type="standard", probability=None):

        if not probability:
            if mutation_type == "weak":
                probability = 1/(5*self.size)
            elif mutation_type == "standard":
                probability = 1 / self.size
            elif mutation_type == "strong":
                probability = 5 / self.size

        mask = np.random.random((self.size,)) < probability
        mask_0 = np.logical_and(mask, self.cargo == 0)
        mask_1 = np.logical_and(mask, self.cargo == 1)
        self.cargo[mask_0] = 1
        self.cargo[mask_1] = 0
        self.changed = True



    def crossover(self, other, crossover_type="two_point",self_copy = None):
        if not self_copy:
            self_copy = copy.deepcopy(self)
        self_copy.fitness=self.fitness

        if crossover_type == "standard":
            mask = np.random.randint(2, size=self.size)
            self_copy.cargo = np.where(mask, self.cargo, other.cargo)

        elif crossover_type == "one_point":
            point_var = rn.randint(0,self.size-1)
            self_copy.cargo = np.concatenate((self.cargo[:point_var], other.cargo[point_var:]))


        elif crossover_type == "two_point":
            point_var = rn.sample(range(self.size-2), k=2)
            point_var.sort()
            point_var = [x+1 for x in point_var]
            self_copy.cargo = np.concatenate((self.cargo[:point_var[0]], other.cargo[point_var[0]:point_var[1]],self.cargo[point_var[1]:]))

        elif crossover_type == "empty":
            self_copy = rn.choice([self_copy,copy.deepcopy(other)])


        if (self.cargo != self_copy.cargo).all():
            self_copy.changed = True

        return self_copy

