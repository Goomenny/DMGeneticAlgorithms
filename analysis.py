import _pickle as pickle
import numpy as np

from matplotlib import pyplot as plt
import os
path = "E:/stats/"
pfiles = os.listdir(path)
# for pfunc in pfiles:
#     pdims = os.listdir(path+pfunc+"/")
#     for pdim in pdims:
#         pparams = os.listdir(path + pfunc+"/"+pdim+"/")
#         for pparam in pparams:
#
#             with open(path + pfunc+"/"+pdim+"/"+pparam, 'rb') as f:
#                 stats = pickle.load(f)
#
#             fitnesses = np.array(stats["fit"])
#             fig = plt.figure()
#             plt.plot(np.max(fitnesses, 2).mean(0), color="r")
#
#             plt.plot(np.mean(fitnesses, 2).mean(0), color="r")
#
#             plt.plot(np.percentile(fitnesses, axis=2, q=50).mean(0), color="black")
#
#             plt.plot(np.min(fitnesses, 2).mean(0), color="r")
#
#             plt.show()


with open("E:/stats/schwefel52d/dynamic#tournament_2#two_point#weak_stats.pickle", 'rb') as f:
            stats = pickle.load(f)

            fitnesses = np.array(stats["fit"])
            x = np.array(stats["x"])
            #fitnesses = [fitnesses]
            print(x[:,300])
            fig = plt.figure()
            plt.plot(np.max(fitnesses, 2).mean(0), color="r")

            plt.plot(np.mean(fitnesses, 2).mean(0), color="r")

            plt.plot(np.percentile(fitnesses, axis=2, q=50).mean(0), color="black")

            plt.plot(np.min(fitnesses, 2).mean(0), color="r")

            plt.show()