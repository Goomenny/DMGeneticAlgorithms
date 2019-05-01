
from keras.layers import Dense, LSTM, Dropout, SimpleRNN, GRU, RepeatVector,Embedding
from keras.models import Model
import keras.backend as K
from keras.layers import Input
#prepping the data



inp = Input(shape=(maxlen,))
a = Embedding(max_features, 100)(inp)
b = LSTM(5,return_sequences=True)(a)
b = LSTM(3,return_sequences=False)(b)
c = Dense(46, activation='softmax')(b)
model = Model(inputs=inp, outputs=c)

model.compile(optimizer='Adagrad', loss='categorical_crossentropy', metrics=['acc'])
model.summary()
history = model.fit(partial_x_train, partial_y_train,
                    epochs=1,
                    batch_size=1208,
                    validation_split=.2)
print(history.history["val_loss"])
import random as rn




# n=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# nn=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# print(n.get_formula())
# print(nn.get_formula())
# n.offspring[0].crossover(nn.offspring[0])
# print(n.get_formula())
# print(n.get_architecture())
# n.compile()


# from Tree import NeuralTree
#
# tr = NeuralTree(max_depth=2, growth="full")
# tr.compile(max_features,maxlen)

# inp = Input(shape=(32,))
# a = RepeatVector(3)(inp)
# model = n.evaluate([a],n.number_rnns())
#
# print(model.summary())

# inp = Input(shape=(32,))
# a = RepeatVector(3)(inp)
# b = Dense(64)(a)
# c = SimpleRNN(32,return_sequences=True)(b)
# d = Dense(32)(c)
# e = GRU(5,return_sequences=True)(d)
# print(d)