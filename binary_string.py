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
        for x in self.cargo:

            self.cargo[x] = other.cargo[x].copy()
        self.fitness = other.fitness

    def calculate_result(self):
        for dim,n in self.N.items():
            summa = sum(self.cargo[n[1]-n[0]:n[1]] * 2 ** np.arange(n[0]))
            self.dec[dim] = self.bounds[dim][0]+summa*self.E[dim]*0.1

    def calculate_result2(self):
        for dim,genotype in self.cargo.items():
            summa = 0
            for i,gen in enumerate(genotype):
                summa += 2**i*int(gen)
            # summa = sum(genotype * 2 ** np.arange(len(genotype)))
            self.dec[dim] = self.bounds[dim][0]+summa*self.E[dim]*0.1

    def get_result(self):
        self.calculate_result()
        return [x for x in self.dec.values()]

    def calculate_fitness(self, obj_func):

        self.fitness = 1 / (1 + obj_func(self.get_result))
        self.changed = True

    def mutate(self, mutation_type="standard", probability=None):

        if not probability:
            if mutation_type is "weak":
                probability = 1/(5*self.size)
            elif mutation_type is "standard":
                probability = 1 / self.size
            elif mutation_type is "strong":
                probability = 5 / self.size

        mask = np.random.random_sample((self.size,)) < probability
        self.cargo[np.logical_and(mask, self.cargo == 1)] = 0
        self.cargo[np.logical_and(mask, self.cargo == 0)] = 1
        # for i in range(self.size):
        #     if rn.random() < probability:
        #         self.changed = True
        #         if self.cargo[i] == 0:
        #             self.cargo[i] = 1
        #         else:
        #             self.cargo[i] = 0

    def mutate2(self, mutation_type="standard", probability=None):

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
                    self.changed = True
                    if self.cargo[dim][i] == 0:
                        self.cargo[dim][i] = 1
                    else:
                        self.cargo[dim][i] = 0

    def crossover(self, other, crossover_type="two_point",self_copy = None):
        if not self_copy:
            self_copy = copy.deepcopy(self)
        self_copy.fitness=self.fitness

        if crossover_type is "standard":
            mask = np.random.randint(2, size=self.size)
            self_copy.cargo[mask] = other.cargo[mask]
            # for i in range(self.size):
            #     if rn.random() < 0.5:
            #         self_copy.cargo[i] = other.cargo[i]
            #     else:
            #         self_copy.cargo[i] = self.cargo[i]
        elif crossover_type is "one_point":
            point_var = rn.randint(0,self.size-1)
            flag = False
            for i in range(self.size):
                if point_var == i:
                    flag = True
                elif flag:
                    self_copy.cargo[i] = other.cargo[i]
                else:
                    self_copy.cargo[i] = self.cargo[i]

        elif crossover_type is "two_point":
            point_var = rn.randint(0,self.size-1)


            while True:
                second_point_var = rn.randint(0,self.size-1)
                if point_var != second_point_var:
                    break

            flag = False
            second_flag = False
            for i in range(self.size):
                if point_var == i  or second_point_var == i:

                    if not flag:
                        flag = True
                    elif not second_flag:
                        second_flag = True

                if flag and not second_flag:
                    self_copy.cargo[i] = other.cargo[i]
                else:
                    self_copy.cargo[i] = self.cargo[i]
        elif crossover_type is "empty":
            self_copy = rn.choice([self_copy,copy.deepcopy(other)])


        if (self.cargo != self_copy.cargo).all():
            self_copy.changed = True

        return self_copy

    def crossover2(self, other, crossover_type="two_point",self_copy = None):
        if not self_copy:
            self_copy = copy.deepcopy(self)
        self_copy.fitness=self.fitness

        if crossover_type is "standard":
            for dim, genotype in self.cargo.items():
                for i, gen in enumerate(genotype):
                    if rn.random() < 0.5:
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
                    else:
                        self_copy.cargo[dim][i] = self.cargo[dim][i]
        elif crossover_type is "one_point":
            point_var = rn.choice(list(self.cargo.keys()))
            point_gen = rn.choice([i+1 for i in range(len(self.cargo[point_var])-1)])
            flag = False
            for dim, genotype in self.cargo.items():
                for i, gen in enumerate(genotype):
                    if point_var is dim and point_gen is i:
                        flag = True
                    elif flag:
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
                    else:
                        self_copy.cargo[dim][i] = self.cargo[dim][i]

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
                            flag = False
                        elif not flag: flag = True

                    if flag:
                        self_copy.cargo[dim][i] = other.cargo[dim][i]
                    else:
                        self_copy.cargo[dim][i] = self.cargo[dim][i]
        elif crossover_type is "empty":
            self_copy = rn.choice([self_copy,copy.deepcopy(other)])

        for var,val in self.cargo.items():
            if (val != self_copy.cargo[var]).all():
                self_copy.changed = True
                break

        return self_copy

if __name__ == "__main__":
    import random
    random.seed(64)
    b1 = binary_string(bounds=[[-1,1]])
    b2 = binary_string(bounds=[[-1, 1]])
    print(b1.cargo)
    print(b2.cargo)
    b1= b1.crossover(b2,"standard")
    print(b1.cargo)
    b1.mutate()
    print(b1.cargo)