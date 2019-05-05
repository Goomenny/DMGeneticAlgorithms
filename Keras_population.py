from population import Population
from Keras_Tree import Keras_Tree
from multiprocessing import Pool,freeze_support
class Keras_Population(Population):
    def __init__(self,
                 algorithm = None,
                 sizeofpopulation=100,
                 objective_function=None,
                 variables=None,
                 bounds = None,
                 type_selection = None,
                 type_crossover = None,
                 type_mutation = None,
                 max_depth = None):

        super().__init__(algorithm = algorithm,
                 sizeofpopulation=sizeofpopulation,
                 objective_function=objective_function,
                 variables=variables,
                 bounds = bounds,
                 type_selection = type_selection,
                 type_crossover = type_crossover,
                 type_mutation = type_mutation)

        for i in range(self.size):
            self.individuums.append(Keras_Tree(max_depth=max_depth, growth="part", variables=variables))
            self.trial_individuums.append(Keras_Tree(max_depth=max_depth, growth="part", variables=variables))

    def multi_calculating_fitness(self, i, trial = False):
        if trial:
            return self.objective_function(self.trial_individuums[i].get_result)
        else:
            return self.objective_function(self.individuums[i].get_result)


    def calculate_fitnesses(self,trial=False):

        if not trial:
            individuums = self.individuums
        else:
            individuums = self.trial_individuums

        freeze_support()
        with Pool(processes=8) as pool:
            multiple_results = [pool.apply_async(self.multi_calculating_fitness,(i,trial,)) for i in range(self.size)]
            val_loss = []
            for res in multiple_results:
                val_loss.append(res.get())
            for i,ind in enumerate(self.individuums):
                ind.fitness = 1 / (1 + val_loss[i])
