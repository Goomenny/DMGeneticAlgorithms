from genalgorithm import GeneticAlgorithm
import _pickle as pickle
import os
from multiprocessing import Pool, TimeoutError
import numpy as np
import problem
# # определяем текущий каталог и печатаем
# path = os.getcwd()
# print ("Текущая рабочая директория %s" % path)
class Test:
    def __init__(self, runs = 100,size_of_population = 100,iterations = 200):

        self.runs = runs
        self.size_of_population = size_of_population
        self.iterations = iterations


    def start_parallel1(self,obj_funcs,bounds):

        with Pool(processes=1) as pool:
            # self.fitnesses=pool.map(self.objective_function,[ind.get_result for ind in self.individuums])
            multiple_results = [pool.apply_async(self.do_test, (obj_func,bound,)) for obj_func,bound in zip(obj_funcs,bounds)]
            for res in multiple_results:
                res.get()

    def do_test(self,obj_func,bounds,param,path):
        fit = []
        x = []
        for run in range(self.runs):
            ga = GeneticAlgorithm(algorithm="ga",
                                  objective_function=obj_func,
                                  bounds=bounds,
                                  selfconfiguration=param[1],
                                  scheme=param[0],
                                  size_of_population=self.size_of_population,
                                  iterations=self.iterations,
                                  type_selection=param[2],
                                  type_crossover=param[3],
                                  type_mutation=param[4],
                                  nprint=-1)
            ga.run()
            fit.append(ga.fit_stats)
            x.append(ga.x_stats)
            print(param[0],run)
        fit = np.array(fit)
        x = np.array(x)
        np.savez(path + "/" + ga.name, fit=fit, sol=x)
        print("Успешно записан %s" % ga.name)


    def start_parallel(self,obj_funcs,bounds,params):
        all_combinations = []
        # params = [["dynamic", True, "rank", "standard", "weak"],
        #           ["standard", True, "rank", "standard", "weak"]
        #           ]
        for obj_func, bound in zip(obj_funcs, bounds):

            path = "stats_tests"+str(self.size_of_population)+str(self.iterations)+"/"+obj_func.__name__+"/"+str(len(bound))+"d"
            try:
                os.makedirs(path)
            except OSError:
                print("Создать директорию %s не удалось" % path)
            else:
                print("Успешно создана директория %s" % path)

            for param in params:
                all_combinations.append((obj_func,bound,param,path,))



        with Pool(processes=2) as pool:
            multiple_results = [pool.apply_async(self.do_test, parameters) for parameters in all_combinations]
            for res in multiple_results:
                res.get()

    def gp_start_parallel(self,obj_funcs,params):
        all_combinations = []
        # params = [["dynamic", True, "rank", "standard", "weak"],
        #           ["standard", True, "rank", "standard", "weak"]
        #           ]
        for obj_func in obj_funcs:

            path = "GPstats_tests"+str(self.size_of_population)+str(self.iterations)+"/"+obj_func.__name__+"/"+str(obj_func.dim)+"d"
            try:
                os.makedirs(path)
            except OSError:
                print("Создать директорию %s не удалось" % path)
            else:
                print("Успешно создана директория %s" % path)

            for param in params:
                all_combinations.append((obj_func,param,path,))



        with Pool(processes=2) as pool:
            multiple_results = [pool.apply_async(self.do_test_, parameters) for parameters in all_combinations]
            for res in multiple_results:
                res.get()
    def do_test_(self,obj_func,param,path):

        fit = []
        gp = []
        for run in range(self.runs):
            gp.append(GeneticAlgorithm(algorithm="gp",
                                  objective_function=obj_func,
                                  selfconfiguration=param[1],
                                  scheme=param[0],
                                  variables=obj_func.variables,
                                  size_of_population=self.size_of_population,
                                  max_depth=5,
                                  iterations=self.iterations,
                                  type_selection=param[2],
                                  type_crossover=param[3],
                                  type_mutation=param[4],
                                  nprint=-1))
        for i in range(self.runs):
            gp[i].run()
            fit.append(gp[i].fit_stats)

            print(param[0], i)

        fit = np.array(fit)

        np.savez(path + "/" + gp[0].name, fit=fit)
        print("Успешно записан %s" % gp[0].name)




