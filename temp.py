#
# from keras.layers import Dense, LSTM, Dropout, SimpleRNN, GRU, RepeatVector,Embedding
# from keras.models import Model
# import keras.backend as K
# from keras.layers import Input
# #prepping the data
# from keras.utils import to_categorical
# from keras.datasets import reuters
# from keras.preprocessing import sequence
# #
# max_features = 1000  # number of words to consider as features
# maxlen = 200  # cut texts after this number of words (among top max_features most common words)
# batch_size = 32
#
# print('Loading data...')
# (input_train, y_train), (input_test, y_test) = reuters.load_data(num_words=max_features)
# print(len(input_train), 'train sequences')
# print(len(input_test), 'test sequences')
#
# print('Pad sequences (samples x time)')
# input_train = sequence.pad_sequences(input_train, maxlen=maxlen)
# input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
# print('input_train shape:', input_train.shape)
# print('input_test shape:', input_test.shape)
#
# #one hot encode labes
# one_hot_train_labels = to_categorical(y_train)
# one_hot_test_labels = to_categorical(y_test)
#
# #train test
# partial_x_train = input_train
#
# partial_y_train = one_hot_train_labels
#
# #train test
# x_test = input_test
# print(x_test.shape)
# y_test = one_hot_test_labels
#
# inp = Input(shape=(maxlen,))
# a = Embedding(max_features, 100)(inp)
# b = LSTM(50,return_sequences=True)(a)
# b = LSTM(30,return_sequences=False)(b)
# c = Dense(46, activation='softmax')(b)
# model = Model(inputs=inp, outputs=c)
#
# model.compile(optimizer='Adagrad', loss='categorical_crossentropy', metrics=['acc'])
# model.summary()
# history = model.fit(partial_x_train, partial_y_train,
#                     epochs=1,
#                     batch_size=1208,
#                     validation_split=.2)
# print(history.history["val_loss"])
import random as rn
# class problem():
#     def __init__(self, obj_func):
#         self.obj_func = obj_func
#         self.variables  = [maxlen,max_features]
#         # self.__name__ = obj_func.__name__
#     def __str__(self):
#         return self.__name__
#     def __call__(self, get_model):
#         model = get_model(self.variables)
#         history = model.fit(self.obj_func[0], self.obj_func[1],
#                             epochs=1,
#                             batch_size=128,
#                             validation_split=.2)
#         del model  # for avoid any trace on aigen
#         K.clear_session()  # removing session, it will instance another
#         return  history.history["val_loss"][0]
#
#
# import genalgorithm
# pr = problem([partial_x_train[::40], partial_y_train[::40]])
# gp = genalgorithm.GeneticAlgorithm(algorithm="gp",
#                                        objective_function=pr,
#                                        variables=pr.variables,
#                                        selfconfiguration=False,
#                                        size_of_population = 10,
#                                        iterations=20,
#                                        type_selection="tournament_9",
#                                        type_crossover="one_point",
#                                        type_mutation="growth",
#                                         nprint=1)
# gp.run()
# # n=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# # nn=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# # print(n.get_formula())
# # print(nn.get_formula())
# # n.offspring[0].crossover(nn.offspring[0])
# # print(n.get_formula())
# # print(n.get_architecture())
# # n.compile()
#
#
from SR_Tree import SR_Tree




import problem as pr

from scipy.optimize import minimize
from matplotlib import pyplot as plt
from SR_Tree_Optimizer import SR_Tree_Optimizer
optimizer = SR_Tree_Optimizer()

tr = SR_Tree(max_depth=5, growth="part",variables=["x0"])
print(pr.objective_function(tr.get_result))
print(tr.get_formula())

func = tr.get_result
x = []
real = []
aprox = []
for var,y in pr.data:
    x.append(var["x0"])
    real.append(y)
    aprox.append(func(var))

fig = plt.figure()
plt.scatter(x,real,s=1)
plt.scatter(x, aprox,s=1)
plt.show()


optimizer.optimize(tr,pr.objective_function)
print(pr.objective_function(tr.get_result))
print(tr.get_formula())


func = tr.get_result
x = []
real = []
aprox = []
for var,y in pr.data:
    x.append(var["x0"])
    real.append(y)
    aprox.append(func(var))

fig = plt.figure()
plt.scatter(x,real,s=1)
plt.scatter(x, aprox,s=1)
plt.show()

# # inp = Input(shape=(32,))
# # a = RepeatVector(3)(inp)
# # b = Dense(64)(a)
# # c = SimpleRNN(32,return_sequences=True)(b)
# # d = Dense(32)(c)
# # e = GRU(5,return_sequences=True)(d)
# # print(d)