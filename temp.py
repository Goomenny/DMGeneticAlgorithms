#
# from keras.layers import Dense, LSTM, Dropout, SimpleRNN, GRU, RepeatVector,Embedding
# from keras.models import Model
# import keras.backend as K
# from keras.preprocessing import sequence
# from keras.datasets import reuters
# from keras.layers import Input
# from keras.utils import to_categorical
# import numpy as np
# #prepping the data
# max_features = 1000  # number of words to consider as features
# maxlen = 200  # cut texts after this number of words (among top max_features most common words)
# batch_size = 64
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
# # one hot encode labes
# one_hot_train_labels = to_categorical(y_train)
# one_hot_test_labels = to_categorical(y_test)
#
# # train test
# partial_x_train = input_train
#
# partial_y_train = one_hot_train_labels
#
# # train test
#
# x_test = input_test
# print(x_test.shape)
# y_test = one_hot_test_labels
#
# inp = Input(shape=(maxlen,))
# a = Embedding(max_features, 100)(inp)
# print(a)
# b = GRU(14,return_sequences=True,activation="elu")(a)
# b =Dropout(0.4)(b)
# b = GRU(14,return_sequences=True,activation="elu")(b)
# b = Dense(42,activation="sigmoid")(b)
# b = GRU(43,return_sequences=True,activation="sigmoid")(b)
# b = GRU(40,return_sequences=False,activation="elu")(b)
# # b = SimpleRNN(2,return_sequences=True,activation="linear")(a)
# # b = SimpleRNN(29,return_sequences=True,activation="elu")(b)
# # b = SimpleRNN(49,return_sequences=True,activation="tanh")(b)
# # b = GRU(39,return_sequences=True,activation="selu")(b)
# # b = GRU(47,return_sequences=False,activation="softplus")(b)
# c = Dense(46, activation='softmax')(b)
# model = Model(inputs=inp, outputs=c)
#
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
# model.summary()
# history = model.fit(partial_x_train[::10], partial_y_train[::10],
#                     epochs=5,
#                     batch_size=batch_size,validation_data=(input_test,y_test))
# print("Val_acc = %s" % history.history["val_acc"])
# prediction = model.predict(x_test)
# print ( [np.argmax(i) for i in prediction])




# n=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# nn=NeuralNode(deep=0, node_type=True, max_depth=2,variables=[1,2],growth="full")
# print(n.get_formula())
# print(nn.get_formula())
# n.offspring[0].crossover(nn.offspring[0])
# print(n.get_formula())
# print(n.get_architecture())
# n.compile()


from Keras_Tree import Keras_Tree
tree = Keras_Tree(max_depth=3,growth="part")
tree.changed=False
print(tree.get_size())
print(tree.get_formula(),tree.changed)
tree.mutate("standard")
print(tree.get_formula(),tree.changed)

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