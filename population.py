
from binary_string import binary_string
import random as rn
import copy


import os


class Population:
    def __init__(self,
                 algorithm = None,
                 sizeofpopulation=100,
                 objective_function=None,
                 variables=None,
                 bounds = None,
                 type_selection = None,
                 type_crossover = None,
                 type_mutation = None):

        self.objective_function = objective_function
        self.individuums = []
        self.trial_individuums = []
        self.proportionalprob = []
        self.rankprob = []
        self.parents = []
        self.bestInd = None
        # Номер лучшего индивида
        self.i_best = None
        self.size = sizeofpopulation
        self.operators = dict(selection=[type_selection for i in range(self.size)],
                              mutation=[type_mutation for i in range(self.size)],
                              crossover=[type_crossover for i in range(self.size)])

        if algorithm is "ga":
            for i in range(self.size):
                self.individuums.append(binary_string(bounds=bounds))
                self.trial_individuums.append(binary_string(bounds=bounds))


    def fitness(self, i, is_trial = False):

        if is_trial:
            return self.trial_individuums[i].fitness
        else:
            return self.individuums[i].fitness

    def get_fitnesses(self):

        return [ind.fitness for ind in self.individuums]

    def proportionalSelection(self):

        summa = sum([ind.fitness for ind in self.individuums])
        self.proportionalprob = [ind.fitness / summa for ind in self.individuums]

    def rankSelection(self):

        sorted_fitnesses = sorted(range(self.size), key=lambda x: self.fitness(x))

        self.rankprob = [None for i in range(self.size)]

        for i, index in enumerate(sorted_fitnesses):
            self.rankprob[index] = 2.0 * (i + 1) / (self.size * (self.size + 1))

    def tournamentSelection(self,size_tour):
        indexes = []
        #indexes = rn.sample(range(self.size), k=size_tour)

        while len(indexes) < size_tour:
            rand = rn.randint(0,self.size-1)
            if rand not in indexes:
                indexes.append(rand)
        #tour = [self.individuums[i] for i in indexes]

        tour_fit = [self.individuums[i].fitness for i in indexes]
        best_index = tour_fit.index(max(tour_fit))

        return self.individuums[indexes[best_index]]

    def dynamic_scheme(self):
        trial_individuums = []
        selection_type, size_tour = self.operators["selection"][0].split("_")
        for i, ind in enumerate(self.individuums):

            while True:

                parent = self.tournamentSelection(int(size_tour))
                if ind != parent:
                    break

            new_ind = ind.crossover(parent, crossover_type=self.operators["crossover"][0])
            new_ind.mutate(mutation_type=self.operators["mutation"][0])
            if new_ind.changed:
                new_ind.calculate_fitness(self.objective_function)
                # new_ind.fitness = 1 / (1 + self.objective_function(new_ind.get_result))

                if new_ind.fitness > ind.fitness:
                    self.individuums[i] = new_ind

    def _getParent(self, selection_type=None):


        if not "tournament" in selection_type:

            if selection_type == "proportional":
                probabilities = self.proportionalprob
            elif selection_type == "rank":
                probabilities = self.rankprob

            rnval = rn.random()
            summa = 0
            for ind, prob in zip(self.individuums, probabilities):
                summa += prob
                if summa > rnval:
                    return ind
        else:
            selection_type, size_tour = selection_type.split("_")
            return self.tournamentSelection(int(size_tour))

    def selection(self):

        self.parents = []

        for i in range(self.size):
            while True:
                parent1, parent2 = self._getParent(self.operators["selection"][i]), self._getParent(
                    self.operators["selection"][i])
                if parent1 != parent2:
                    break

            self.parents.append([parent1, parent2])

    def mutate(self):

        for i, ind in enumerate(self.individuums):
            if self.i_best != i:
                ind.mutate(mutation_type=self.operators["mutation"][i])

    def calculate_fitnesses(self, trial = False):

        if not trial:
            individuums = self.individuums
        else:
            individuums = self.trial_individuums
        for i, ind in enumerate(individuums):
            if ind.changed:
                ind.calculate_fitness(self.objective_function)

    def findBest(self):

        fitnesses = [self.fitness(i) for i in range(self.size)]

        ibest = fitnesses.index(max(fitnesses))
        if self.i_best:
            if fitnesses[ibest] > fitnesses[self.i_best]:
                self.i_best = ibest
        else:
            self.i_best = ibest
        self.bestInd = copy.deepcopy(self.individuums[self.i_best])

    def evolve(self):
        #self.trial_individuums = [None for i in range(self.size)]
        self.i_best = rn.randint(0, self.size - 1)
        self.trial_individuums[self.i_best] = copy.deepcopy(self.bestInd)

        for i,parent in enumerate(self.parents):
            if self.i_best != i:#not self.trial_individuums[i]:
                self.trial_individuums[i] = parent[0].crossover(parent[1], self.operators["crossover"][i],self.trial_individuums[i])
        self.individuums,self.trial_individuums = self.trial_individuums, self.individuums
    def dynamic_evolve(self):

        for i in range(self.size):
            while True:
                parent = self._getParent(self.operators["selection"][i])
                if parent != self.individuums[i]:
                    break
            self.trial_individuums[i] = self.individuums[i].crossover(parent, self.operators["crossover"][i],self.trial_individuums[i])

            self.trial_individuums[i].mutate(mutation_type=self.operators["mutation"][i])

    def best_replacement(self):

        for i in range(self.size):
            if self.trial_individuums[i].fitness > self.individuums[i].fitness:
                self.individuums[i].copy(self.trial_individuums[i])

