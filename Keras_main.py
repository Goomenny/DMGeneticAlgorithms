import genalgorithm
from Keras_problem import problem
from Keras_population import Keras_Population

from multiprocessing import freeze_support
#

import os
if __name__ == '__main__':

    pr = problem()
    gp = genalgorithm.GeneticAlgorithm(algorithm="gp",
                                       class_population=Keras_Population,
                                           objective_function=pr,
                                           variables=pr.variables,
                                           selfconfiguration=True,
                                           size_of_population = 10,
                                           iterations=20,
                                            max_depth=4,
                                            scheme="dynamic",
                                           type_selection="tournament_9",
                                           type_crossover="one_point",
                                           type_mutation="growth",
                                            nprint=1)
    gp.run()