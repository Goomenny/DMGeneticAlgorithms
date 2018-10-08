

import cProfile
from builtins import print

from matplotlib import pyplot as plt

import numpy as np
#rn.seed(7)
import genalgorithm, problem
import ndtestfuncs
import tests
import ndtestfuncs as tfunc

class problem():
    def __init__(self, obj_func):
        self.obj_func = obj_func
        self.__name__ = obj_func.__name__
    def __call__(self, x):
        return self.obj_func(x())




if __name__ == '__main__':

    # gp = GeneticProgramming(objective_function=objective_function,variables=variables)

    test =  tests.Test()
    dims = [5,10]
    allfuncnames = tfunc.funcnames_minus()
    allfuncs = [problem(func) for func in tfunc.allfuncs_minus()]
    allbounds = []
    for dim in dims:
        allbounds += [[tuple(tfunc.getbounds(func.__name__,dim)) for d in range(dim)] for func in allfuncs]
    allfuncs *=len(dims)


    test.start_parallel(allfuncs,allbounds)
    # ga = genalgorithm.GeneticAlgorithm(algorithm="ga",
    #                                    objective_function=allfuncs[0],
    #                                    bounds=allbounds[0],
    #                                    selfconfiguration=False,
    #                                    size_of_population = 100,
    #                                    iterations=100,
    #                                    type_selection="tournament_5",
    #                                    type_crossover="two_point",
    #                                    type_mutation="weak",
    #                                    nprint=5)
    #gp = GP.GeneticProgramming("gp",objective_function=problem.objective_function, variables=problem.variables)
    #ga.run_dynamic()
    #cProfile.run("ga.run()", sort="cumtime")
    # fitnesses = ga.fit_stats
    # stats = ga.oper_stats
    # fitnesses =[fitnesses]
    # print(np.array(ga.fit_stats).shape)
    # gp=ga
    # определим имя директории, которую создаём






    # func = gp.population.bestInd.get_result
    # x = []
    # real = []
    # aprox = []
    # for var,y in problem.data:
    #     x.append(var["x0"])
    #     real.append(y)
    #     aprox.append(func(var))
    #
    # fig = plt.figure()
    # plt.scatter(x,real,s=1)
    # plt.scatter(x, aprox,s=1)
    # plt.show()
    #
    # if stats:
    #     operator = "selection"
    #     x = []
    #     for i in range(stats["size"]):
    #         x.append(i)
    #
    #     fig = plt.figure()
    #     ax = {}
    #     for i,operator in enumerate(stats):
    #         if operator != "size":
    #             ax[operator] = plt.subplot(2, 2, i+1)
    #             plt.title(operator)
    #             plt.grid()
    #             for type in stats[operator]:
    #                 ax[operator].plot(x,stats[operator][type]["probability"],label = type)
    #
    #
    #             chartBox = ax[operator].get_position()
    #             ax[operator].set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
    #             ax[operator].legend(loc='upper center', bbox_to_anchor=(0.1, 0.9), shadow=True, ncol=1)
    #     plt.show()
    # #

