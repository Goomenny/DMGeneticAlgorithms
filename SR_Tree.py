import copy
import random as rn
from Tree import Tree
from SR_Node import SR_Node
from SR_Tree_Optimizer import SR_Tree_Optimizer
class SR_Tree(Tree):
    def __init__(self,
                 max_depth=1,
                 growth="full",
                 variables = None):
        super().__init__(max_depth, growth, variables)
        self.root = SR_Node(deep=0, node_type=True, max_depth=self.max_depth,variables=self.variables,growth=growth)


    def __str__(self):
        return str(self.root)

    def copy(self,other):
        self.root= copy.deepcopy(other.root)
        self.fitness = other.fitness

    def get_result(self, var):
        return self.root.evaluate(var)

    def get_formula(self):
        return self.root.get_formula()

    def get_depth(self):

        return self.root.get_depth()
    def calculate_fitness(self, obj_func, coefficient_optimized = False):
        if coefficient_optimized:
            optimizer = SR_Tree_Optimizer()
            optimizer.optimize(self,obj_func)
        self.fitness = 1 / (1 + obj_func(self.get_result))

    def mutate(self, mutation_type = "standard",probability =None):
        super().mutate(mutation_type, probability, SR_Node)
