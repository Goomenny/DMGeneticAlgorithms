import random as rn
from Node import Node
map_operators = ("Union",
                 "Dropout")

map_layers = ("Dense",
              "LSTM",
              "SimpleRNN",
              "GRU")

rnsize_neurons = lambda: (rn.randint(1, 50))
rnsize_drop = lambda: (rn.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]))
map_activations = ("softmax", "elu", "selu", "softplus", "softsign", "relu", "tanh", "sigmoid", "hard_sigmoid",
                   "linear")


class Keras_Node(Node):
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
            self.cargo = rn.choice(list(map_operators))
            self.arity = 2
            self.size_drop = rnsize_drop()
        else:
            self.arity = 0

            self.cargo = rn.choice(list(map_layers))
            self.size_neurons = rnsize_neurons()
            self.activation = rn.choice(map_activations)
            self.variable = False

        self.parent = parent
        self.offspring = []
        if self.type:
            for i in range(self.arity):
                self.offspring.append(Keras_Node(parent=self,
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
                for node in self.offspring[:-1]:
                    formula += node.get_formula()

                    if self.cargo == "Dropout":
                        formula += str(self.cargo)
                        formula += "\t" + str(self.size_drop)
                        formula += "\n"
                formula += self.offspring[-1].get_formula()
                formula += "\n"
                return formula
        else:
            return str(self.cargo) + "\t" + str(self.size_neurons) + "\t" + str(self.activation) + "\n"

    def get_architecture(self):
        if self is None: return

        arch = []
        if self.type:
            for node in self.offspring[:-1]:
                offspring_layers = node.get_architecture()
                for layer in offspring_layers:
                    arch.append(layer)
                if self.cargo == "Dropout":
                    arch.append([self.cargo, self.size_drop])

            offspring_layers = self.offspring[-1].get_architecture()
            for layer in offspring_layers:
                arch.append(layer)

            return arch
        else:
            return [[self.cargo, self.size_neurons, self.activation]]

    def number_rnns(self):

        if self.type:
            return self.offspring[0].number_rnns() + self.offspring[1].number_rnns()
        else:
            if self.cargo in ["LSTM", "SimpleRNN", "GRU"]:
                return 1
            else:
                return 0

    def mutate(self, probability):
        changed = False

        if self.type:
            if rn.random() < probability:
                self.cargo = rn.choice(list(map_operators))
                changed = True
            for ind in self.offspring:
                if ind.mutate(probability):
                    changed = True
        else:
            if rn.random() < probability:
                self.cargo = rn.choice(list(map_layers))
                changed = True
            if rn.random() < probability:
                self.size_neurons = rnsize_neurons()
                changed = True
            if rn.random() < probability:
                self.activation = rn.choice(map_activations)
                changed = True

        return changed