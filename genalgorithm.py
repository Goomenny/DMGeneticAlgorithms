import numpy as np
from multiprocessing import Pool
from Keras_population import Keras_Population as Population
import random as rn
class GeneticAlgorithm:
    def __init__(self,
                 algorithm = None,
                 size_of_population=100,
                 objective_function = None,
                 iterations = 100,
                 variables = None,
                 bounds = None,
                 selfconfiguration = False,
                 nprint = 1,
                 type_selection = None,
                 type_crossover = None,
                 type_mutation = None,
                 scheme = "standard"):
        self.scheme = scheme
        self.algorithm = algorithm
        self.selfconfiguration = selfconfiguration
        self.objective_function = objective_function
        self.population = Population(algorithm = algorithm,
                                     sizeofpopulation=size_of_population,
                                     objective_function=objective_function,
                                     variables=variables,
                                     bounds=bounds,
                                     type_selection=type_selection,
                                     type_crossover=type_crossover,
                                     type_mutation=type_mutation
                                     )

        self.name = algorithm+"#"+scheme+"#"
        if self.selfconfiguration:
            self.name += "selfconfiguration"
        else:
            self.name += "notselfconf"
            self.name += "#"+type_selection+"#"+type_crossover+"#"+type_mutation

        self.selection_type = []
        self.mutation_type = []
        self.crossover_type = []
        self.iterations = iterations
        self.edge = 0.1

        self.nprint = nprint

        if algorithm is "ga":
            self.operators = dict(selection=("proportional", "rank", "tournament_9", "tournament_5", "tournament_2"),
                                  mutation=("weak","standard","strong"),
                                  crossover=("standard", "one_point","two_point"))
        elif algorithm is "gp":
            self.operators = dict(selection=("proportional", "rank", "tournament_3", "tournament_5", "tournament_9"),
                                  mutation=("growth", "weak", "standard", "strong"),
                                  crossover=("standard", "one_point"))

        self.fit_stats = []
        self.x_stats = []
        self.oper_stats = {operator:{type: dict(probability=[]) for type in self.operators[operator]} for operator in self.operators}
        self.oper_stats["size"] = self.iterations
        self.reset_probabilities()


    def save_selfconf_probabilities(self):

        for operator in self.params:
            for type in self.params[operator]:
                self.oper_stats[operator][type]["probability"].append(self.params[operator][type]["probability"])

    def print_iter_stats(self,i):

        if i % self.nprint == 0 and self.nprint != -1:
            fitnesses = np.array(self.population.get_fitnesses())
            print("Mean", fitnesses.mean(), "Std", fitnesses.std(), "Mode", np.percentile(fitnesses, 50))
            print(i, self.population.bestInd.fitness, self.objective_function(self.population.bestInd.get_result))
            if self.algorithm == "ga":
                print(self.population.bestInd.get_result())
            elif self.algorithm == "gp":
                print(self.population.bestInd.get_formula())
    def reset_probabilities(self):

        self.params = {operator:{type: dict(probability=1 / len(self.operators[operator]), average_fitness=0, amount = 0) for type in self.operators[operator]}  for operator in self.operators }

    def recount_probabilities(self, is_trial = False, include_best=True):

        for operator, types in self.params.items():
            for type in types:
                self.params[operator][type]["amount"] = self.population.operators[operator].count(type)
                if include_best and self.population.operators[operator][self.population.i_best] is type:
                    self.params[operator][type]["amount"] -= 1


        for operator, types in self.population.operators.items():
            for i, type in enumerate(types):
                if self.params[operator][type]["amount"] != 0 and i != self.population.i_best:
                    self.params[operator][type]["average_fitness"] += self.population.fitness(i,is_trial=is_trial) / self.params[operator][type]["amount"]

        for operator, types in self.params.items():
            extra_probability = 0
            best_type = None
            for type in types:
                if not best_type:
                    best_type = type
                elif self.params[operator][type]["average_fitness"] > self.params[operator][best_type]["average_fitness"]:
                    best_type = type
                if self.params[operator][type]["probability"] < self.edge + 1/(len(types) * self.iterations) and  self.params[operator][type]["probability"] > self.edge:
                    extra_probability += self.params[operator][type]["probability"] - self.edge
                    self.params[operator][type]["probability"] = self.edge
                elif self.params[operator][type]["probability"] > self.edge + 1/(len(types) * self.iterations):
                    extra_probability += 1/(len(types)*self.iterations)
                    self.params[operator][type]["probability"] -= 1/(len(types)*self.iterations)
            self.params[operator][best_type]["probability"] += extra_probability

    def select_operators(self):

        for operator in self.params:
            new_types = []
            for i in range(self.population.size):
                rnval = rn.random()
                summa = 0
                for type in self.params[operator]:
                    summa += self.params[operator][type]["probability"]
                    if summa > rnval:
                        new_types.append(type)
                        break
            self.population.operators[operator] = new_types

    def add_stats(self):

        self.fit_stats.append(self.population.get_fitnesses())
        if self.algorithm == "ga":
            self.x_stats.append(self.population.bestInd.get_result())

    def run_standard(self):

        if self.selfconfiguration:
            self.select_operators()
            self.save_selfconf_probabilities()

        self.population.calculate_fitnesses()
        self.population.findBest()
        self.add_stats()
        for i in range(self.iterations):

            self.print_iter_stats(i)

            self.population.proportionalSelection()
            self.population.rankSelection()

            if i > 0 and self.selfconfiguration:
                self.recount_probabilities()
                self.select_operators()
                self.save_selfconf_probabilities()


            self.population.selection()
            self.population.evolve()
            self.population.mutate()

            self.population.calculate_fitnesses()
            self.population.findBest()
            self.add_stats()

    def run_dynamic(self):

        if self.selfconfiguration:
            self.select_operators()
            self.save_selfconf_probabilities()

        self.population.calculate_fitnesses()
        self.population.findBest()
        self.add_stats()

        for i in range(self.iterations):

            self.print_iter_stats(i)

            self.population.proportionalSelection()
            self.population.rankSelection()

            if i > 0 and self.selfconfiguration:
                self.recount_probabilities(is_trial=True,include_best=False)
                self.select_operators()
                self.save_selfconf_probabilities()

            self.population.dynamic_evolve()
            self.population.best_replacement()

            self.population.findBest()
            self.add_stats()

    def run(self):

        if self.scheme == "dynamic":
            self.run_dynamic()
        elif self.scheme == "standard":
            self.run_standard()
