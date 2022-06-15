import geneticAlgorithmTC as gaTC
import numpy as np
import calendar
import plot
from config import *
from calendarFunctions import *
import time

if __name__ == "__main__":
    
    # tasksGeneral = {MONDAY: [TOB, CK], TUESDAY: [TIB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[], SATURDAY:[], SUNDAY: [VS]}
    tasksGeneral = {MONDAY: [CTB], TUESDAY: [CTB],  WEDNESDAY: [CTB], THURSDAY:[CTB], FRIDAY:[CTB], SATURDAY:[CTB], SUNDAY: [CTB]}
    tasksLenght = sum([len(tasks) for tasks in list(tasksGeneral.values())])
    people = np.array(list(DAYSOFF.keys()))
    peopleGeneral = people[[ALBERTO, OSCAR, ANDRIU, ZARRA, AYDEN, BISWU, CEREN, HATICE, SEDA, EMMA, ALAN, DAVOR, SERGIO] ]
    currentCalendar = calendar.monthcalendar(YEAR, MONTH)
    calendarStarts = getAddition(tasksGeneral.items(), currentCalendar)
    
    load = False
    ntests = 1
    for config in ["config{}".format(i) for i in range(6, 7)]:
        bestScoresTests = []
        fit1Tests = []
        fit2Tests = []
        fit3Tests = []
        fit4Tests = []
        fit5Tests = []
        start = time.time()
        for ntest in range(ntests):
            print("\n\n\n", config, " ntest: ", ntest, "\n\n")
            ga = gaTC.GA(currentCalendar, tasksGeneral, peopleGeneral, 
                            configs[config]["population"], mutationGeneProb=configs[config]["mutationGeneProb"], typeSelection = ROULETTE, 
                            typeMutation = configs[config]["typeMutation"], typeCrossover = configs[config]["typeCrossover"], 
                            mutationProb = configs[config]["mutationProb"], uniformCross = configs[config]["uniformCrossValue"], load=load)
            bestScores = ga.trainGA(configs[config]["iterations"])
            bestScoresTests.append(bestScores[0])
            fit1Tests.append(bestScores[1])
            fit2Tests.append(bestScores[2])
            fit3Tests.append(bestScores[3])
            fit4Tests.append(bestScores[4])
            fit5Tests.append(bestScores[5])
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/bestScores/bestScores_{}_test{}.jpg".format(config, ntests), "Best Chromosome Fitness", bestScoresTests, True)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/bestScores/bestScoresAvg_{}_test{}.jpg".format(config, ntests), "Best Chromosome Fitness", bestScoresTests, True)
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit1/bestfit1_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 1", fit1Tests)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit1/bestfit1Avg_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 1", fit1Tests)
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit2/bestfit2_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 2", fit2Tests)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit2/bestfit2Avg_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 2", fit2Tests)
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit3/bestfit3_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 3", fit3Tests)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit3/bestfit3Avg_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 3", fit3Tests)
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit4/bestfit4_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 4", fit4Tests)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit4/bestfit4Avg_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 4", fit4Tests)
        plot.bestScoresPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit5/bestfit5_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 5", fit5Tests)
        plot.bestScoresAvgPlotTests("CalendarioAlgoritmoGenetico/data/graphs/fit5/bestfit5Avg_{}_test{}.jpg".format(config, ntests), "Chromosome Fitness 5", fit5Tests)
        printChromosome(ga.best.info, calendarStarts, currentCalendar, tasksLenght, tasksGeneral, YEAR, MONTH)

        end = time.time() - start
        with open("CalendarioAlgoritmoGenetico/data/graphs/execTime{}_test{}.txt".format(config, ntests), "w+") as f:
            f.write("Execution Time: {}".format(end))

