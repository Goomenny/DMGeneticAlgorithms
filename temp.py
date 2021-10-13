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


# from Keras_Tree import Keras_Tree
# tree = Keras_Tree(max_depth=3,growth="part")
# tree.changed=False
# print(tree.get_size())
# print(tree.get_formula(),tree.changed)
# tree.mutate("standard")
# print(tree.get_formula(),tree.changed)

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

"""
===============
Rain simulation
===============

Simulates rain drops on a surface by animating the scale and opacity
of 50 scatter points.

Author: Nicolas P. Rougier
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create rain data
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(50, 200, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none')


def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    rain_drops['position'][current_index] = np.random.uniform(0, 1, 2)
    rain_drops['size'][current_index] = 5
    rain_drops['color'][current_index] = (0, 0, 0, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()