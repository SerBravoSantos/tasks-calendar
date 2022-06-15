import matplotlib.pyplot as plt
import numpy as np

def bestScoresPlot(file, title, bestScores):

    plt.title(title)
    plt.plot(bestScores)
    plt.yticks(np.arange(0.75, 1, step=0.025))
    plt.grid()
    plt.savefig(file)
    plt.close()

def bestScoresPlotTests(file, title, bestScoresTests, yticks=False):
    plt.title(title)
    for bestScores in bestScoresTests:
        plt.plot(bestScores)
    if yticks:
        plt.yticks(np.arange(0.75, 1, step=0.025))
    plt.grid()
    plt.savefig(file)
    plt.close()

def bestScoresAvgPlotTests(file, title, bestScoresTests, yticks=False):
    plt.title(title) 
    plt.plot([np.mean(bestScores) for bestScores in zip(*bestScoresTests)])
    if yticks:
        plt.yticks(np.arange(0.75, 1, step=0.025))
    plt.grid()
    plt.savefig(file)
    plt.close()