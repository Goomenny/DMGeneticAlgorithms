import copy
import random as rn
from Tree import Tree
from Keras_Node import Keras_Node
from keras.layers import Dense, LSTM, Dropout, SimpleRNN, GRU, RepeatVector,Embedding
from keras.models import Model
from keras.layers import Input

map_layers = {"Dense":Dense,
             "LSTM": LSTM,
             "SimpleRNN" : SimpleRNN,
             "GRU": GRU}

class Keras_Tree(Tree):
    def __init__(self,
                 max_depth=1,
                 growth="full",
                 variables = None):
        super().__init__(max_depth, growth, variables)
        self.root = Keras_Node(deep=0, node_type=True, max_depth=self.max_depth, variables=self.variables, growth=growth)
        while (self.root.number_rnns()<1):
            super().mutate("strong",Node_class=Keras_Node)
    def copy(self,other):
        self.root= copy.deepcopy(other.root)
        self.fitness = other.fitness

    def compile(self,var):
        architecture = self.root.get_architecture()
        number_rnns = self.root.number_rnns()
        return_seq = True
        layers = []

        layers.append(Input(shape=(var[0],)))
        layers.append(Embedding(var[1], 100)(layers[-1]))

        for layer_conf in architecture:
            if number_rnns <= 1:
                return_seq = False
            if layer_conf[0] == "Dropout":
                layers.append(Dropout(layer_conf[1])(layers[-1]))
            elif layer_conf[0] == "Dense":
                layers.append(map_layers[layer_conf[0]](layer_conf[1],activation =layer_conf[2])(layers[-1]))
            else:
                layers.append(map_layers[layer_conf[0]](layer_conf[1], activation=layer_conf[2], return_sequences=return_seq)(layers[-1]))
                number_rnns -= 1
        layers.append(Dense(46, activation='softmax')(layers[-1]))
        model = Model(inputs=layers[0], outputs=layers[-1])

        model.compile(optimizer='Adagrad', loss='categorical_crossentropy', metrics=['acc'])
        #model.summary()
        return model


    def get_result(self, var):
        return self.compile(var)

    def mutate(self, mutation_type = "growth",probability =None):

        if not probability:
            if mutation_type == "weak":
                probability = 1/(3*5*self.get_size())
            elif mutation_type == "standard":
                probability = 1 / (3*self.get_size())
            elif mutation_type == "strong":
                probability = 5 / (3*self.get_size())

        super().mutate(mutation_type,probability,Keras_Node)
        while (self.root.number_rnns()<1):
            super().mutate("strong",Node_class=Keras_Node)