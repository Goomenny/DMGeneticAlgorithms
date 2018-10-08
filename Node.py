import random as rn
import copy
import math

# OPERATORS = {'+': (lambda x, y: x + y), '-': (lambda x, y: x - y),
#              '*': (lambda x, y: x * y), '/': (lambda x, y: x / y)}

import operator
OPERATORS = {'+': (operator.add), '-': (operator.sub),
             '*': (operator.mul), '/': (operator.truediv)}

rncargo = lambda: (rn.random() * 2 - 1)


class Node:
    def __init__(self,
                 node_type=None,
                 func=None,
                 parent=None,
                 deep=None,
                 max_depth=None,
                 variables = None,
                 growth = None):

        self.variables = variables
        if node_type is None:
            if deep >= max_depth:
                self.type = False
            elif growth == "full":
                self.type = True
            else:
                self.type = rn.choice([True, False])
        else:
            self.type = node_type

        self.deep = deep
        self.arn = 2
        self.func = func
        if self.type:
            self.cargo = rn.choice(list(OPERATORS.keys()))
        else:
            if rn.choice([True, False]):
                self.cargo = rncargo()
                self.variable = False
            else:
                self.variable = True
                self.cargo = rn.choice(self.variables)
        self.parent = parent
        self.offspring = []
        if self.type:
            for i in range(self.arn):
                self.offspring.append(Node(parent=self,
                                           deep=deep + 1,
                                           max_depth=max_depth,
                                           variables=self.variables,
                                           growth=growth))

    def __str__(self):
        return str(self.cargo)

    def resetDeep(self, deep=0):
        self.deep = deep
        if self.type:
            for child in self.offspring:
                child.resetDeep(self.deep + 1)

    def get_formula(self):
        if self is None: return


        if self.type:
            formula = ""
            formula += "("
            for node in self.offspring[:-1]:
                formula += node.get_formula()
                formula += self.cargo
            formula += self.offspring[-1].get_formula()
            formula += ")"
            return formula
        else:
            return str(self.cargo)


    def evaluate(self, var):
        if self.type:

            try:
                return OPERATORS[self.cargo](self.offspring[0].evaluate(var), self.offspring[1].evaluate(var))
            except ZeroDivisionError:
                return 1000000
        elif self.variable:
            return var[self.cargo]
        else:
            return self.cargo

    def crossover(self, other, deepcopy=True):
        if deepcopy:
            newnode = copy.deepcopy(other)
        else:
            newnode = other
        newnode.parent = self.parent
        self.parent.offspring[self.parent.offspring.index(self)] = newnode
        newnode.resetDeep(newnode.parent.deep + 1)
        self = newnode

    def getSimilarNodes(self,other):

        if self.type == other.type:

            if self.type:
                nodes = [[self, other]]
                offspring_nodes = []
                for self_offspring,other_offspring in zip(self.offspring,other.offspring):
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
            elif self.variable == other.variable:
                return [self,other]
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
    def mutate(self, probability):

        if rn.random() < probability:
            if self.type:

                self.cargo = rn.choice(list(OPERATORS.keys()))
            elif self.variable:
                self.variable = False
                self.cargo = rncargo()
            else:
                self.variable = True
                self.cargo = rn.choice(self.variables)
            return True
        flag = False
        for ind in self.offspring:
            if ind.mutate(probability):
                flag = True
        return flag