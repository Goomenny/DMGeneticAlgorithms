import _pickle as pickle
import numpy as np
import pandas as pn
from matplotlib import pyplot as plt
import os
from sklearn.metrics import mean_squared_error
from ndtestfuncs import getminpoint,name_to_func
from math import fabs
def reliability(func_name,x_aprox):
    step = 50
    n = int(x_aprox.shape[1] / step)
    reliab = [0]*(n+1)
    mse = 0
    mfmin = 0
    minpoint = getminpoint(func_name,x_aprox.shape[-1])
    fmin = name_to_func[func_name](minpoint)
    # if func_name == "ellipse" and x_aprox.shape[-1]==2:
    #         print("f")
    for iter in x_aprox:
        for i in range(n):
            if (abs(minpoint - iter[i*step]) < 0.01).all():
                reliab[i] += 1
        if (abs(minpoint - iter[-1]) < 0.01).all():
            reliab[-1] += 1

        mse += mean_squared_error(iter[-1],minpoint)
        mfmin += name_to_func[func_name](iter[-1])
    reliab = [r/ x_aprox.shape[0] for r in reliab ]
    mse /= x_aprox.shape[0]
    mfmin /= x_aprox.shape[0]
    return reliab, mse, mfmin, fmin
def pltfigures():
    path = "C:/Users/goome/YandexDisk/учеба/Магдип/stats_np400800/"
    pfiles = os.listdir(path)

    for pfunc in pfiles:
        pdims = os.listdir(path+pfunc+"/")
        if "powersum" not in pfunc:
            ax={}
            fig = plt.figure()
            #plt.suptitle(pfunc[0].capitalize()+pfunc[1::])
            for d,pdim in enumerate(pdims):

                pparams = os.listdir(path + pfunc+"/"+pdim+"/")


                ax[pdim]=plt.subplot(2, 2, d + 1)
                plt.title(pdim, fontsize=11)

                # try:
                #     os.makedirs("E:/stats_np2/" + pfunc + "/" + pdim + "/")
                # except:
                #     pass
                for i,pparam in enumerate(pparams):
                    if "selfconfiguration" in pparam:
                        with np.load(path + pfunc+"/"+pdim+"/"+pparam, 'r') as data:
                            #stats= pickle.load(data)
                            fitnesses = data["fit"]
                            x = data["sol"]
                            # fitnesses = np.array(stats["fit"])
                            # x_sol = np.array( [[ [x for x in sol.values()] for sol in iter] for iter in stats["x"]])
                            # try:
                            #     np.savez("E:/stats_np3/" + pfunc+"/"+pdim+"/"+"ga#standard#selfconfiguration",fit=fitnesses,sol=x)
                            # except:
                            #     print("Ошибка")
                            # print("E:/stats_np3/" + pfunc+"/"+pdim+"/"+"ga#standard#selfconfiguration", "saved")
                            reliab = []
                            try:
                                reliab, mse, mfmin, fmin = reliability(pfunc, x)
                                print(pfunc+ " " + pdim,pparam,"reliab",reliab,"mse %f" %mse,"mfmin %f"%mfmin, "fmin %f" %fmin)
                            except:
                                print(pfunc+ " " + pdim,pparam,"ошибка")
                            color , linestyle = 'b', '--'
                            if "dynamic" in pparam:
                                color, linestyle = 'r', ':'
                            pparam = pparam.replace("ga#","").replace("dynamic","best replacement").replace("notselfconf#","").replace("#","/").replace(".npz","")

                            #ax[pdim].plot(np.array([list(map(name_to_func[pfunc], xi)) for xi in x]).mean(0), label=pparam,color = color,linestyle=linestyle)
                            ax[pdim].plot( np.array([i*50 for i in range(len(reliab))]),np.array(reliab) ,label=pparam, color=color, linestyle=linestyle)
                            #ax[pdim].plot(,np.array(reliab), label=pparam, color=color, linestyle=linestyle)
                            chartBox = ax[pdim].get_position()
                            ax[pdim].set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
                            # if "standard" in pparam:
                            #     plt.plot(np.max(fitnesses, 2).T,color='b')
                            #     # plt.plot(np.array([list(map(name_to_func[pfunc], xi)) for xi in x]).T, color='b')
                            #
                            # elif "dynamic" in pparam:
                            #     # plt.plot(np.array([list(map(name_to_func[pfunc], xi)) for xi in x]).T, color='r')
                            #     plt.plot(np.max(fitnesses, 2).T, color='r')
                plt.grid()
                #plt.semilogy()
                plt.ylabel('reliability')
                plt.xlabel('population')

            plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=1)

            fig.tight_layout()
            plt.subplots_adjust(wspace=0.07)
            # fig.savefig('D:/YandexDisk/учеба/IWMMA/2018/300i600p_%s.png' %pfunc)
            plt.show()

def pltreliability():
    path = "E:/stats_notself/"

    pfiles = os.listdir(path)
    for pfunc in pfiles:
        pdims = os.listdir(path + pfunc + "/")
        if "powersum" not in pfunc:

            for d, pdim in enumerate(pdims):

                pparams = os.listdir(path + pfunc + "/" + pdim + "/")

                for i, pparam in enumerate(pparams):
                    if "ga" in pparam:
                        with np.load(path + pfunc + "/" + pdim + "/" + pparam, 'r') as data:

                            fitnesses = data["fit"]
                            x = data["sol"]
                            pparam = pparam.replace("ga#", "").replace("dynamic", "best replacement").replace(
                                "notselfconf#", "").replace("#", "/").replace(".npz", "")

                            try:
                                reliab, mse, mfmin, fmin = reliability(pfunc, x)
                                print(pfunc+ " " + pdim,pparam,"reliab",reliab[0],reliab[1],reliab[2],reliab[3],reliab[4],reliab[5],reliab[6],"mse %f" %mse,"mfmin %f"%mfmin, "fmin %f" %fmin)
                            except:
                                print(pfunc+ " " + pdim,pparam,"ошибка")

def plotreliabilities():
    df= pn.read_csv("reliabilities.csv",sep="\t")
    #fig=plt.figure()
    #df.plot(kind='line',x='Population')
    ax = plt.gca()

    df.plot(kind='line', x='Population', y='best replacement/selfconfiguration', color= 'r',linestyle=":",ax=ax)
    df.plot(kind='line', x='Population', y='standard/selfconfiguration',color= 'b', linestyle="--",ax=ax)


    plt.ylabel('Reliability')
    plt.grid()
    plt.tight_layout()
    plt.show()
def autolabel(rects,ax):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%f' % h,
                ha='center', va='bottom')


def pltbars():



    path = "E:/stats_np3/"

    pfiles = os.listdir(path)
    for pfunc in pfiles:
        pdims = os.listdir(path + pfunc + "/")
        for pdim in pdims:
            pparams = os.listdir(path + pfunc + "/" + pdim + "/")
            fig = plt.figure()
            plt.title(pfunc + "/" + pdim)
            N = 1
            ind = np.arange(N)  # the x locations for the groups
            width = 0.2  # the width of the bars


            ax = fig.add_subplot(111)
            rects = []
            for i, pparam in enumerate(pparams):

                with np.load(path + pfunc + "/" + pdim + "/" + pparam, 'r') as data:
                    # stats= pickle.load(data)
                    fitnesses = data["fit"]
                    x = data["sol"]

                    yvals = [np.max(fitnesses, 2).mean(0)[-1]]
                    rects.append(ax.bar(ind+width*i, yvals, width))
                    autolabel(rects[i],ax)
                    #plt.bar(ind*i, np.max(fitnesses, 2).mean(0), label=pparam)
            #plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.1), shadow=True, ncol=1)
            ax.set_ylabel('Fitness')
            #ax.set_xticks(ind + width)
            #ax.set_xticklabels(range(len(pparams)))
            ax.legend(rects,pparams)
            plt.grid()
            plt.show()
    #
    # yvals = [4]
    # rects1 = ax.bar(ind, yvals, width, color='r')
    # zvals = [1]
    # rects2 = ax.bar(ind + width, zvals, width, color='g')
    # kvals = [11]
    # rects3 = ax.bar(ind + width * 2, kvals, width, color='b')
    #
    # ax.set_ylabel('Scores')
    # ax.set_xticks(ind + width)
    # ax.set_xticklabels(('2011-Jan-4', '2011-Jan-5', '2011-Jan-6'))
    # ax.legend((rects1[0], rects2[0], rects3[0]), ('y', 'z', 'k'))
    #
    #
    #
    # autolabel(rects1)


    # plt.show()


if __name__ == '__main__':
    pltfigures()
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