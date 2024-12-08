import matplotlib.pyplot as plt
import numpy as np

"""The functions for plotting the results are found here
"""

def bestScoresPlot(file, title, bestScores):
    """Plots a graph showing the best scores achieved by the ga among the iterations it trained for
    
        Args:
            file (str): path to the file where we will save the plot
            title (str): title of the plot
            bestScores (list[float]): array of scores
    """
    plt.title(title)
    plt.plot(bestScores)
    plt.yticks(np.arange(0.75, 1, step=0.025))
    plt.grid()
    plt.savefig(file)
    plt.close()

def bestScoresAvgPlotTests(file, title, bestScoresTests, cuts=None, fileParh=None, yticks=False):
    """Plots a graph showing the mean of the best scores achieved by the ga among the iterations it trained for
    
        Args:
            file (str): path to the file where we will save the plot
            title (str): title of the plot
            bestScoresTests (list[float]): array of scores
            cuts (int): bests score in the iteration indicated
            fileParh (str): path of the file where we want to write the cut
            yticks (Bool): True if we want to represent the y ticks aswell
    """
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