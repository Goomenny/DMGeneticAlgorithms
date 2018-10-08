from genalgorithm import GeneticAlgorithm
import _pickle as pickle
import os
from multiprocessing import Pool, TimeoutError
import problem
# # определяем текущий каталог и печатаем
# path = os.getcwd()
# print ("Текущая рабочая директория %s" % path)
class Test:
    def __init__(self, runs = 100):

        self.runs = runs


    def start_parallel(self,obj_funcs,bounds):

        with Pool(processes=8) as pool:
            # self.fitnesses=pool.map(self.objective_function,[ind.get_result for ind in self.individuums])
            multiple_results = [pool.apply_async(self.do_test, (obj_func,bound,)) for obj_func,bound in zip(obj_funcs,bounds)]
            for res in multiple_results:
                res.get()




    def do_test(self,obj_func,bounds):

        path = "E:/stats/"+obj_func.__name__+"/"+str(len(bounds))+"d"

        try:
            os.makedirs(path)
        except OSError:
            print("Создать директорию %s не удалось" % path)
        else:
            print("Успешно создана директория %s" % path)
        fit = []
        x = []
        for run in range(self.runs):
            ga = GeneticAlgorithm(algorithm="ga",
                                  objective_function=obj_func,
                                  bounds=bounds,
                                  selfconfiguration=False,
                                  size_of_population=100,
                                  iterations=300,
                                  type_selection="tournament_9",
                                  type_crossover="two_point",
                                  type_mutation="weak",
                                  nprint=-1)
            ga.run()
            fit.append(ga.fit_stats)
            x.append(ga.x_stats)

        stats = {"fit":fit,"x":x}

        with open(path+'/standard#tournament_9#two_point#weak_stats.pickle', 'wb') as f:
            try:
                pickle.dump(stats, f)
                print("Успешно записан "+ path+'/standard#tournament_9#two_point#weak_stats.pickle')
            except:
                print("Ошибка сохранения")




