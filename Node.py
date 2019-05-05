import copy

class Node:
    def __init__(self,
                 node_type=None,
                 parent=None,
                 deep=None,
                 max_depth=None,
                 variables=None,
                 growth=None):

        self.type: bool

        self.deep: int

        self.arity: int

        self.cargo: str
        self.variable: bool

        self.offspring: list
        self.parent: Node

    def __str__(self):
        return str(self.cargo)

    def resetDeep(self, deep=0):
        self.deep = deep
        if self.type:
            for child in self.offspring:
                child.resetDeep(self.deep + 1)

    def crossover(self, other, deepcopy=True):
        if deepcopy:
            newnode = copy.deepcopy(other)
        else:
            newnode = other
        newnode.parent = self.parent
        self.parent.offspring[self.parent.offspring.index(self)] = newnode
        newnode.resetDeep(newnode.parent.deep + 1)
        self = newnode

    def getSimilarNodes(self, other):

        if self.type == other.type:

            if self.type and self.arity == other.arity:
                nodes = [[self, other]]
                offspring_nodes = []
                for self_offspring, other_offspring in zip(self.offspring, other.offspring):
                    tmp = self_offspring.getSimilarNodes(other_offspring)
                    if tmp:
                        if type(tmp[0]) is list:
                            for i in tmp:
                                offspring_nodes.append(i)
                        else:
                            offspring_nodes.append(tmp)
                if offspring_nodes:
                    nodes += offspring_nodes
                return nodes
            elif not self.type and self.variable == other.variable:
                return [self, other]
            else:
                return
        else:
            return

    def get_depth(self, deep=0):

        if self.type:

            mass = [node.get_depth() for node in self.offspring]

            return max(mass)

        else:
            return self.deep

    def getNodesFromLayer(self, deep):

        if self.deep == deep:
            return [self]
        else:
            nodes = []
            for node in self.offspring:
                nodes += node.getNodesFromLayer(deep)
            if nodes:
                return nodes
            else:
                return []
    def get_number_offsprings(self):
        size = 0

        if self.type:

            mass = [node.get_number_offsprings() for node in self.offspring]

            return sum(mass)+1

        else:
            return 1

