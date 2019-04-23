from population import Population
import random as rn

class SR_Population(Population):
    def __init__(self,
                 algorithm=None,
                 sizeofpopulation=100,
                 objective_function=None,
                 variables=None,
                 bounds=None,
                 type_selection=None,
                 type_crossover=None,
                 type_mutation=None,
                 max_depth = None):
        super().__init__(algorithm = algorithm,
                                     sizeofpopulation=sizeofpopulation,
                                     objective_function=objective_function,
                                     variables=variables,
                                     bounds=bounds,
                                     type_selection=type_selection,
                                     type_crossover=type_crossover,
                                     type_mutation=type_mutation,
                                     max_depth = max_depth
                                     )

    def calculate_fitnesses(self, trial = False):
        if not trial:
            individuums = self.individuums
        else:
            individuums = self.trial_individuums
        for i, ind in enumerate(individuums):
            if ind.changed:
                if i == self.i_best:
                    ind.calculate_fitness(self.objective_function,coefficient_optimized=True)
                elif rn.random()<1:
                    ind.calculate_fitness(self.objective_function, coefficient_optimized=False)
                else:
                    ind.calculate_fitness(self.objective_function)