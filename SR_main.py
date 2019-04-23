import cProfile

from matplotlib import pyplot as plt
import random as rn
#rn.seed(66)
import genalgorithm
import tests
import time
import problem as pr
from problem import problem
import testfuncs_semenkina as tfunc

if __name__ == '__main__':

    #gp = GeneticProgramming(objective_function=objective_function,variables=variables)

    test =  tests.Test()
    dims = [2]
    #allfuncnames = tfunc.funcnames_minus()
    #allfuncs = [problem(func) for func in tfunc.allfuncs_minus()]

    allfuncs = [problem(func,2) for func in tfunc.getfuncs(names="myfunc")]
    allfuncs *=len(dims)
    params = [["dynamic", True, "rank", "standard", "weak"],
              ["standard", True, "rank", "standard", "weak"]
              ]
    if False:
        t1=time.time()
        test.gp_start_parallel(allfuncs,params)
        print(time.time()-t1)
    else:
        gp = genalgorithm.GeneticAlgorithm(algorithm="gp",
                                           objective_function=allfuncs[0],
                                           variables=allfuncs[0].variables,
                                           selfconfiguration=True,
                                           scheme="dynamic",
                                           size_of_population = 100,
                                           iterations=200,
                                           max_depth = 5,
                                           type_selection="tournament_9",
                                           type_crossover="one_point",
                                           type_mutation="growth",
                                            nprint=10)

        t1=time.time()
        gp.run()
        print(time.time()-t1)
    # cProfile.run("gp.run()", sort="tottime")
    # fitnesses = ga.fit_stats
    # stats = ga.oper_stats
    # fitnesses =[fitnesses]
    # print(np.array(ga.fit_stats).shape)
    # gp=ga
    # определим имя директории, которую создаём


    #
    # func = gp.population.bestInd.get_result
    # x = []
    # real = []
    # aprox = []
    # for var,y in allfuncs[0].data:
    #     x.append(var["x0"])
    #     real.append(y)
    # aprox.append(func(allfuncs[0].np_var))
    #
    # fig = plt.figure()
    # plt.scatter(x,real,s=1)
    # plt.scatter(x, aprox,s=1)
    # plt.show()

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