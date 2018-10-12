import math
import random as rn
import copy
class binary_string:
    def __init__(self,
                 bounds = None):
        self.accuracy = 0.001
        self.E = {}
        self.bounds = {}
        self.cargo = {}
        self.dec = {}
        for dim,bound in enumerate(bounds):
            N = math.log((bound[1]-bound[0])/(0.1*self.accuracy))/math.log(2)
            if int(N) != N:
                N = int(N+1)
            else:
                N = int(N)
            self.cargo["x"+str(dim)] = [rn.choice([0,1]) for i in range(N)]
            self.E["x" + str(dim)] = (bound[1]-bound[0])/(2**N*0.1)
            self.bounds["x" + str(dim)] = [bound[0],bound[1]]
        self.fitness = None
        self.changed = True
        self.size = sum([len(val) for val in self.cargo.values()])

    def __str__(self):
        return str(self.get_result())

    def calculate_result(self):
        for dim,genotype in self.cargo.items():
            summa = 0
            for i,gen in enumerate(genotype[::-1]):
                summa += 2**i*int(gen)

            self.dec[dim] = self.bounds[dim][0]+summa*self.E[dim]*0.1

    def get_result(self):
        self.calculate_result()
        return [x for x in self.dec.values()]

    def calculate_fitness(self, obj_func):

        self.fitness = 1 / (1 + obj_func(self.get_result))
    def mutate(self, mutation_type="standard", probability=None):

        if not probability:
            if mutation_type is "weak":
                probability = 1/(5*self.size)
            elif mutation_type is "standard":
                probability = 1 / self.size
            elif mutation_type is "strong":
                probability = 5 / self.size

        for dim, genotype in self.cargo.items():
            for i, gen in enumerate(genotype):
                if rn.random() < probability:
                    if self.cargo[dim][i] == 0:
                        self.cargo[dim][i] = 1
                    else:
                        self.cargo[dim][i] = 0


    def crossover(self, other, crossover_type="two_point"):
        self_copy = copy.deepcopy(self)

        if crossover_type is "standard":
            for dim, genotype in self.cargo.items():
                for i, gen in enumerate(genotype):
                    if rn.choice([True,False]):
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
        elif crossover_type is "one_point":
            point_var = rn.choice(list(self.cargo.keys()))
            point_gen = rn.choice([i+1 for i in range(len(self.cargo[point_var])-1)])
            flag = False
            for dim, genotype in self.cargo.items():
                for i, gen in enumerate(genotype):
                    if point_var is dim and point_gen is i:
                        flag = True
                        break
                    else:
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
                if flag:
                    break
        elif crossover_type is "two_point":
            point_var = rn.choice(list(self.cargo.keys()))
            point_gen = rn.choice([i + 1 for i in range(len(self.cargo[point_var]) - 1)])

            while True:
                second_point_var = rn.choice(list(self.cargo.keys()))
                second_point_gen = rn.choice([i + 1 for i in range(len(self.cargo[second_point_var]) - 1)])
                if point_var is not second_point_var or second_point_gen is not point_gen:
                    break

            flag = False
            second_flag = False
            for dim, genotype in self.cargo.items():
                for i, gen in enumerate(genotype):
                    if point_var is dim and point_gen is i or second_point_var is dim and second_point_gen is i:

                        if flag:
                            second_flag = True
                            break
                        elif not flag: flag = True

                    if flag:
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
                if second_flag:
                    break
        elif crossover_type is "empty":
            self_copy = rn.choice([self_copy,copy.deepcopy(other)])
        return self_copy