import genalgorithm
from Keras_problem import problem
from keras.datasets import reuters
from keras.preprocessing import sequence
from keras.utils import to_categorical
from multiprocessing import freeze_support
#

import os
if __name__ == '__main__':
    # вызов функции
    max_features = 1000  # number of words to consider as features
    maxlen = 200  # cut texts after this number of words (among top max_features most common words)
    batch_size = 32

    print('Loading data...')
    (input_train, y_train), (input_test, y_test) = reuters.load_data(num_words=max_features)
    print(len(input_train), 'train sequences')
    print(len(input_test), 'test sequences')

    print('Pad sequences (samples x time)')
    input_train = sequence.pad_sequences(input_train, maxlen=maxlen)
    input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
    print('input_train shape:', input_train.shape)
    print('input_test shape:', input_test.shape)

    # one hot encode labes
    one_hot_train_labels = to_categorical(y_train)
    one_hot_test_labels = to_categorical(y_test)

    # train test
    partial_x_train = input_train

    partial_y_train = one_hot_train_labels

    # train test
    x_test = input_test
    print(x_test.shape)
    y_test = one_hot_test_labels

    pr = problem([partial_x_train[::40], partial_y_train[::40]])
    gp = genalgorithm.GeneticAlgorithm(algorithm="gp",
                                           objective_function=pr,
                                           variables=pr.variables,
                                           selfconfiguration=False,
                                           size_of_population = 10,
                                           iterations=20,
                                           type_selection="tournament_9",
                                           type_crossover="one_point",
                                           type_mutation="growth",
                                            nprint=1)
    gp.run()