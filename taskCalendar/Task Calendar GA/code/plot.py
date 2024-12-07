import matplotlib.pyplot as plt
import numpy as np

def bestScoresPlot(file, title, bestScores):

    plt.title(title)
    plt.plot(bestScores)
    plt.yticks(np.arange(0.75, 1, step=0.025))
    plt.grid()
    plt.savefig(file)
    plt.close()

def bestScoresAvgPlotTests(file, title, bestScoresTests, cuts=None, fileParh=None, yticks=False):
    plt.title(title) 
    for bestScores in bestScoresTests:
        plt.plot(bestScores, color='black', ls='--', linewidth=1)
    means = [np.mean(bestScores) for bestScores in zip(*bestScoresTests)]
    plt.plot(means, color='r', ls='-', linewidth=1)
    if yticks:
        plt.yticks(np.arange(0, 1, step=0.05))
    plt.grid()
    plt.savefig(file)
    plt.close()
    if fileParh:
        with open(fileParh, "w+") as f:
            for i, mean in enumerate(means):
                if i+1 in cuts:
                    f.write("cut {}: ".format(i+1)+ str(mean)+"\n")