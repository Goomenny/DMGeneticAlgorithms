import keras.backend as K

max_features = 1000  # number of words to consider as features
maxlen = 200  # cut texts after this number of words (among top max_features most common words)
batch_size = 32
class problem():
    def __init__(self, obj_func):
        self.obj_func = obj_func
        self.variables  = [maxlen,max_features]
        # self.__name__ = obj_func.__name__
    def __str__(self):
        return self.__name__
    def __call__(self, get_model):

        model = get_model(self.variables)
        history = model.fit(self.obj_func[0], self.obj_func[1],
                            epochs=1,
                            batch_size=128,
                            validation_split=.2, verbose=0)
        del model  # for avoid any trace on aigen
        K.clear_session()  # removing session, it will instance another
        return  history.history["val_loss"][0]