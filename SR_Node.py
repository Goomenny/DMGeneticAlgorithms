import random as rn
import operator
import math
import numpy as np
from Node import Node
pow2 = lambda x: (operator.pow(x,2))
OPERATORS = {'+': (operator.add, 2), '-': (operator.sub, 2),
             '*': (operator.mul, 2), '/': (operator.truediv, 2)}

OPERATORS['pow2'] =  (pow2, 1)
OPERATORS['cos'] = (np.cos,1)
OPERATORS['exp'] = (np.exp,1)

rncargo = lambda: (rn.random() * 2 - 1)




class SR_Node(Node):
    def __init__(self,
                 node_type=None,
                 parent=None,
                 deep=None,
                 max_depth=None,
                 variables=None,
                 growth=None):

        super().__init__(node_type, parent, deep, max_depth, variables, growth)
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

        if self.type:
            self.cargo = rn.choice(list(OPERATORS.keys()))
            self.arity = OPERATORS[self.cargo][1]
        else:
            self.arity = 0
            if rn.choice([True, False]):
                self.cargo = rncargo()
                self.variable = False
            else:
                self.variable = True
                self.cargo = rn.choice(self.variables)

        self.parent = parent
        self.offspring = []
        if self.type:
            for i in range(self.arity):
                self.offspring.append(SR_Node(parent=self,
                                           deep=deep + 1,
                                           max_depth=max_depth,
                                           variables=self.variables,
                                           growth=growth))

    def get_formula(self):
        if self is None: return

        if self.type:
            if self.arity == 1:
                formula = self.cargo
                formula += "("
                formula += self.offspring[0].get_formula()
                formula += ")"
                return formula
            elif self.arity == 2:
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

    def old_evaluate(self, var):
        if self.type:
            if self.arity == 1:
                try:
                    return OPERATORS[self.cargo][0](self.offspring[0].evaluate(var))
                except OverflowError:
                    return float('inf')
            else:
                try:
                    return OPERATORS[self.cargo][0](self.offspring[0].evaluate(var), self.offspring[1].evaluate(var))
                except:
                    return float('inf')
        elif self.variable:
            return var[self.cargo]
        else:
            return self.cargo
    def evaluate(self, var):
        if self.type:
            if self.arity == 1:
                try:
                    return OPERATORS[self.cargo][0](self.offspring[0].evaluate(var))
                except OverflowError:
                    return float('inf')
            else:
                try:
                    return OPERATORS[self.cargo][0](self.offspring[0].evaluate(var), self.offspring[1].evaluate(var))
                except:
                    return float('inf')
        elif self.variable:
            return var[:,int(self.cargo.replace("x",""))]
        else:
            return self.cargo
    def mutate(self, probability):

        if rn.random() < probability:
            if self.type:
                fl = True
                while fl:
                    self.cargo = rn.choice(list(OPERATORS.keys()))
                    if OPERATORS[self.cargo][1] == self.arity:
                        fl = False
                        break
            elif self.variable:

                variables = self.variables
                if len(variables) > 1:
                    variables.remove(self.cargo)
                self.cargo = rn.choice(variables)
            else:
                self.cargo = rncargo()
            return True
        changed = False
        for ind in self.offspring:
            if ind.mutate(probability):
                changed = True
        return changed
    def get_constant_nodes(self):
        if self is None: return

        arch = []
        if self.type:
            for node in self.offspring[:-1]:
                offspring_layers = node.get_constant_nodes()
                for layer in offspring_layers:
                    arch.append(layer)

            offspring_layers = self.offspring[-1].get_constant_nodes()
            for layer in offspring_layers:
                arch.append(layer)

            return arch
        elif not self.variable:
            return [self]
        else:
            return []