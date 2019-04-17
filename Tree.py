from Node import Node
import random as rn
import copy

from timeit import Timer
class Tree:
    def __init__(self,
                 max_depth=1,
                 growth="full",
                 variables = None):
        self.variables = variables
        self.max_depth = max_depth
        self.fitness = None
        self.changed = True

    @property
    def fitness(self):

        return self._fitness
    @fitness.setter
    def fitness(self, value):
        if value != value:
            self._fitness = 0.0000000000001
        else:
            self._fitness = value


    def __str__(self):
        return str(self.root)

    def get_result(self, var):
        return self.root.evaluate(var)

    def get_formula(self):
        return self.root.get_formula()

    def get_depth(self):

        return self.root.get_depth()
    def calculate_fitness(self, obj_func):

        self.fitness = 1 / (1 + obj_func(self.get_result))

    def crossover(self, other, crossover_type="standard",self_copy = None):
        if not self_copy:
            self_copy = copy.deepcopy(self)
        self_copy.fitness = self.fitness

        if crossover_type == "standard":
            rnlayer = rn.randint(1, other.root.get_depth())
            rnselflayer = rn.randint(1, self_copy.root.get_depth())

            changednode = rn.choice(self_copy.root.getNodesFromLayer(rnselflayer))
            nodeforchange = rn.choice(other.root.getNodesFromLayer(rnlayer))

        elif crossover_type == "one_point":
            common_nodes = self_copy.root.getSimilarNodes(other.root)
            if common_nodes:
                if common_nodes[1:]:
                    changednode, nodeforchange = rn.choice(common_nodes[1:])
            else:
                self_copy.changed = False
                return self_copy


        if crossover_type is "standard" or common_nodes[1:]:
            if changednode.deep + nodeforchange.get_depth() - nodeforchange.deep > self.max_depth:
                self_copy.changed = False
                return self_copy
            else:
                changednode.crossover(nodeforchange)
                self_copy.changed = True
        return self_copy

    def mutate(self, mutation_type = "growth",probability =None, Node_class = None):

        if not probability:
            if mutation_type is "weak":
                probability = 1/(5*self.get_depth())
            elif mutation_type is "standard":
                probability = 1 / self.get_depth()
            elif mutation_type is "strong":
                probability = 5 / self.get_depth()

        if mutation_type is "growth":
            rnselflayer = rn.randint(1, self.root.get_depth())
            node = rn.choice(self.root.getNodesFromLayer(rnselflayer))

            mutatednode = Node_class(deep=0, max_depth=self.max_depth - node.deep,variables=self.variables)

            node.crossover(mutatednode, deepcopy=False)
            self.changed = True

        elif mutation_type in ("weak","standard","strong"):

            if self.root.mutate(probability):
                self.changed = True


