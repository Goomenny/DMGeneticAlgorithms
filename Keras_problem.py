import keras.backend as K
from keras.datasets import reuters
from keras.preprocessing import sequence
from keras.utils import to_categorical
max_features = 1000  # number of words to consider as features
maxlen = 200  # cut texts after this number of words (among top max_features most common words)
batch_size = 128
class problem():
    def __init__(self, obj_func = None):
        self.obj_func = obj_func
        self.variables  = [maxlen,max_features]
        # self.__name__ = obj_func.__name__
    def __str__(self):
        return self.__name__
    def __call__(self, get_model):
        if not self.obj_func:
            #print('Loading data...')
            (input_train, y_train), (input_test, y_test) = reuters.load_data(num_words=max_features)
            #print(len(input_train), 'train sequences')
            #print(len(input_test), 'test sequences')

            #print('Pad sequences (samples x time)')
            input_train = sequence.pad_sequences(input_train, maxlen=maxlen)
            input_test = sequence.pad_sequences(input_test, maxlen=maxlen)
            #print('input_train shape:', input_train.shape)
            #print('input_test shape:', input_test.shape)

            # one hot encode labes
            one_hot_train_labels = to_categorical(y_train)
            one_hot_test_labels = to_categorical(y_test)

            # train test
            partial_x_train = input_train

            partial_y_train = one_hot_train_labels

            # train test
            x_test = input_test
            #print(x_test.shape)
            y_test = one_hot_test_labels

            self.obj_func = [partial_x_train[::40],partial_y_train[::40]]


        model = get_model(self.variables)
        history = model.fit(self.obj_func[0], self.obj_func[1],
                            epochs=1,
                            batch_size=batch_size,
                            validation_split=.2, verbose=1)
        del model  # for avoid any trace on aigen
        K.clear_session()  # removing session, it will instance another
        return  history.history["val_loss"][0]