import _pickle as pickle
import numpy as np

from matplotlib import pyplot as plt
import os
from sklearn.metrics import mean_squared_error
from ndtestfuncs import getminpoint,name_to_func
from math import fabs
def reliability(func_name,x_aprox):
    reliab = 0
    mse = 0
    mfmin = 0
    minpoint = getminpoint(func_name,x_aprox.shape[-1])
    fmin = name_to_func[func_name](minpoint)
    for iter in x_aprox:
        if (minpoint - iter[-1] < 0.01).all():
            reliab += 1
        mse += mean_squared_error(iter[-1],minpoint)
        mfmin += name_to_func[func_name](iter[-1])
    reliab /= x_aprox.shape[0]
    mse /= x_aprox.shape[0]
    mfmin /= x_aprox.shape[0]
    return reliab, mse, mfmin, fmin

path = "E:/stats_np3/"
pfiles = os.listdir(path)
for pfunc in pfiles:
    pdims = os.listdir(path+pfunc+"/")

    for pdim in pdims:
        pparams = os.listdir(path + pfunc+"/"+pdim+"/")
        fig = plt.figure()
        plt.title(pfunc + "/" + pdim)
        # try:
        #     os.makedirs("E:/stats_np2/" + pfunc + "/" + pdim + "/")
        # except:
        #     pass
        for pparam in pparams:

            with np.load(path + pfunc+"/"+pdim+"/"+pparam, 'r') as data:
                #stats= pickle.load(data)
                fitnesses = data["fit"]
                x = data["sol"]
            # fitnesses = np.array(stats["fit"])
            # x_sol = np.array( [[ [x for x in sol.values()] for sol in iter] for iter in stats["x"]])

            # np.savez("E:/stats_np2/" + pfunc+"/"+pdim+"/"+pparam.split(".")[0],fit=fitnesses,sol=x_sol)
            # print(pfunc + " " + pdim, pparam, "saved")
            try:
                print(pfunc+ " " + pdim,pparam,reliability(pfunc,x))
            except:
                print(pfunc+ " " + pdim,pparam,"ошибка")

        #     plt.plot(np.max(fitnesses, 2).mean(0),label = pparam)
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), shadow=True, ncol=1)
        # plt.grid()
        # plt.show()


# with open("E:/stats/schwefel/5d/dynamic#tournament_2#two_point#weak_stats.pickle", 'rb') as f:
#             stats = pickle.load(f)
#
#             fitnesses = np.array(stats["fit"])
#             x = np.array(stats["x"])
#             #fitnesses = [fitnesses]
#             print(x[:,300])
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

            # plt.plot(np.mean(fitnesses, 2).mean(0), color="r")
            #
            # plt.plot(np.percentile(fitnesses, axis=2, q=50).mean(0), color="black")
            #
            # plt.plot(np.min(fitnesses, 2).mean(0), color="r")