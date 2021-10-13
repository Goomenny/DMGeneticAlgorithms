import genalgorithm
from Keras_problem import problem
from Keras_population import Keras_Population
import numpy as np
import time
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
    start = time.time()
    gp.run()

    fit = np.array(gp.fit_stats)

    np.savez(gp.name, fit=fit)
    print("Успешно записан %s, time = %s" % (gp.name, time.time() - start))
    print(gp.population.bestInd.get_formula())
    print(gp.population.bestInd.root.get_architecture())
    with open(f"{gp.name}.txt", 'w', encoding='utf-8') as f:
        f.write(gp.population.bestInd.get_formula())