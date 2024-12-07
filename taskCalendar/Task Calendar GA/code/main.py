from operator import truediv
import geneticAlgorithmTC as gaTC
import numpy as np
import calendar
import plot
from config import *
from calendarFunctions import *
import time
import os
import tensorflow as tf

codePath = os.path.dirname(os.path.realpath(__file__))
dirPath = os.path.abspath(os.path.join(codePath, os.pardir))

graphsPath = os.path.join(dirPath, "data/graphs")
textPath = os.path.join(dirPath, "data/textFiles")

def testConfiguration(filename, config, tasksWeek):
    bestScoresTests = []
    fit1Tests = []
    fit2Tests = []
    fit3Tests = []
    fit4Tests = []
    fit5Tests = [] 
    start = time.time()
    for ntest in range(ntests):
        print("\n\n\n", filename, " ntest: ", ntest, "\n\n")
        ga = gaTC.GA(currentCalendar, tasksWeek, peopleChosen, 
                        config["population"], mutationGeneProb=config["mutationGeneProb"], typeSelection = ROULETTE, 
                        typeMutation = config["typeMutation"], typeCrossover = config["typeCrossover"], 
                        mutationProb = config["mutationProb"], uniformCross = config["uniformCrossValue"], load=load, earlyStop=earlystop)
        bestScores = ga.trainGA(config["iterations"])
        bestScoresTests.append(bestScores[0])
        fit1Tests.append(bestScores[1])
        fit2Tests.append(bestScores[2])
        fit3Tests.append(bestScores[3])
        fit4Tests.append(bestScores[4])
        fit5Tests.append(bestScores[5])

    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "bestScores/bestScores_{}_test{}.jpg".format(filename, ntests)), "Best Chromosome Fitness", bestScoresTests, cuts=config["cuts"], fileParh=os.path.join(textPath, "bestFitnessMean_{}_{}_tests.txt".format(filename, ntests)), yticks=True)
    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "fit1/bestfit1_{}_test{}.jpg".format(filename, ntests)), "Chromosome Fitness 1", fit1Tests)
    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "fit2/bestfit2_{}_test{}.jpg".format(filename, ntests)), "Chromosome Fitness 2", fit2Tests)
    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "fit3/bestfit3_{}_test{}.jpg".format(filename, ntests)), "Chromosome Fitness 3", fit3Tests)
    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "fit4/bestfit4_{}_test{}.jpg".format(filename, ntests)), "Chromosome Fitness 4", fit4Tests)
    plot.bestScoresAvgPlotTests(os.path.join(graphsPath, "fit5/bestfit5_{}_test{}.jpg".format(filename, ntests)), "Chromosome Fitness 5", fit5Tests)
    printChromosome(os.path.join(textPath, "calendars/calendar_{}_{}_{}_{}.txt".format(filename, ntests, YEAR, MONTH)), ga.best.info, calendarStarts, currentCalendar, tasksLenght, tasksWeek, YEAR, MONTH)


    end = time.time() - start
    with open(os.path.join(textPath, "execTime_{}_test{}.txt".format(filename, ntests)), "w+") as f:
        f.write("Execution Time: {}".format(end))

if __name__ == "__main__":

    tasksWeek1 = {MONDAY: [TOB, CK], TUESDAY: [TIB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[], SATURDAY:[], SUNDAY: [VS]}
    tasksWeek2 = {MONDAY: [CTB], TUESDAY: [CTB],  WEDNESDAY: [CTB], THURSDAY:[CTB], FRIDAY:[CTB], SATURDAY:[CTB], SUNDAY: [CTB]}
    
    tasksWeek3 = {MONDAY: [TOB], TUESDAY: [TIB, CBB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[CSB], SATURDAY:[], SUNDAY: [VS]}
    tasksList = [tasksWeek3]
    start = time.time()

    # with tf.device('/CPU:0'):
    #     for taskWeekCalendarNumber, tasksWeek in enumerate(tasksList):
    #         tasksLenght = sum([len(tasks) for tasks in list(tasksWeek.values())])
    #         people = np.array(list(DAYSOFF.keys()))
    #         peopleChosen = [ALBERTO, OSCAR, ANDRIU, ZARRA, BISWU, HATICE, EMMA, SERGIO]
    #         currentCalendar = calendar.monthcalendar(YEAR, MONTH)
    #         calendarStarts = getAddition(tasksWeek.items(), currentCalendar)

    #         load = False
    #         # If you set load to True, make sure to follow the same configuration of the chromosome (year, month, tasks and people)
    #         earlystop = None
    #         ntests = 1
    #         test1 = False
    #         test2 = False
    #         test3 = False
    #         testFinal = True

    #         if test1:
    #             for configName in ["config{}_cross".format(i) for i in range(1, 5)]:
    #                 testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, configsCrossoverTest[configName], tasksWeek)
    #         if test2:
    #             for configName, parameters in configMutationTest.items():
    #                 testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, parameters, tasksWeek)
    #         if test3:
    #             for configName, parameters in configMutationTest2.items():
    #                 testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, parameters, tasksWeek)
    #         if testFinal:
    #             testConfiguration(str(taskWeekCalendarNumber)+'_'+configFinal['name']+'_GPU', configFinal['parameters'], tasksWeek)
    # end = time.time() - start
    # with open(os.path.join(textPath, "CPUtestTime.txt"), "w+") as f:
    #     f.write("time with CPU: {}".format(end))
    # start = time.time()
    with tf.device('/GPU:0'):
        for taskWeekCalendarNumber, tasksWeek in enumerate(tasksList):
            tasksLenght = sum([len(tasks) for tasks in list(tasksWeek.values())])
            people = np.array(list(DAYSOFF.keys())) # We obtain the keys from the DAYSOFF dict so we control that we are not including those people that are not contemplated in the daysoff
            peopleChosen = [ALBERTO, OSCAR, ANDRIU, ZARRA, BISWU, HATICE, EMMA, SERGIO]
            currentCalendar = calendar.monthcalendar(YEAR, MONTH)
            calendarStarts = getAddition(tasksWeek.items(), currentCalendar)

            load = True
            # If you set load to True, make sure to follow the same configuration of the chromosome (year, month, tasks and people)
            earlystop = None
            ntests = 1
            test1 = False
            test2 = False
            test3 = False
            testFinal = True

            if test1:
                for configName in ["config{}_cross".format(i) for i in range(1, 5)]:
                    testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, configsCrossoverTest[configName], tasksWeek)
            if test2:
                for configName, parameters in configMutationTest.items():
                    testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, parameters, tasksWeek)
            if test3:
                for configName, parameters in configMutationTest2.items():
                    testConfiguration(str(taskWeekCalendarNumber)+'_'+configName, parameters, tasksWeek)
            if testFinal:
                testConfiguration(str(taskWeekCalendarNumber)+'_'+configFinal['name']+'_GPU', configFinal['parameters'], tasksWeek)
    end = time.time() - start
    with open(os.path.join(textPath, "GPUtestTime.txt"), "w+") as f:
        f.write("time with GPU: {}".format(end))