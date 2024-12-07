from collections import Counter
from configPygad import *
from calendarFunctionsPygad import *
import calendar
import tensorflow as tf
import numpy as np
import pygad
import math
import time
import random

#   changes
#   Initial population
#   mutation, crossover methods
#   Calendar functions

#   PYGAD, interesting 
#       population: A NumPy array holding the initial population.
#       crossover
#       mutation
#       gene_space = [33, 7, 0.5, 95. 6.3, 0.74]
#       gene_space = [{'low': 1, 'high': 5}, {'low': 0.3, 'high': 1.4}, {'low': -0.2, 'high': 4.5}] 
#       gene_space = [ [1,2,3,4],[1,2,3,4], [1,2,3,4]] where [1,2,3,4] = people
#       stop_criteria=["reach_127.4", "saturate_15"])
#       keep_elitism=2
#       sol_per_pop=5

# First create array for the tasks

# tesks for first calendar by weeks
tasksDict = {MONDAY: [TOB, CK], TUESDAY: [TIB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[], SATURDAY:[], SUNDAY: [VS]}
# length of the tasks array (it includes repetitions)
tasksLenght = sum([len(tasks) for tasks in list(tasksDict.values())])
# People chosen for the calendar
people = [ALBERTO, OSCAR, ANDRIU, ZARRA, AYDEN, BISWU, CEREN, HATICE, SEDA, EMMA, ALAN, DAVOR, SERGIO]
# Calendar we want to fill with the tasks and the people
currentCalendar = calendar.monthcalendar(YEAR, MONTH)
# Get the offset of the calendar
calendarStarts = getAddition(tasksDict.items(), currentCalendar)
# Set of the tasks 
diffTask = len(set([val for values in tasksDict.values() for val in values]))
# Number of tasks per day of the week
taskPerDay = list([len(tasks) for tasks in list(tasksDict.values())])

count = 0
for day in currentCalendar[0]:
    if day != 0:
        dayStart = count
    count += 1

random.seed(15)
initial_population = [[random.choice(people) for week in currentCalendar 
                            for dayPos, dayMonth in enumerate(week) 
                                if dayMonth != 0
                                    for dayOfWeek, tasks in tasksDict.items() 
                                        if dayPos == dayOfWeek
                                            for _ in tasks] for _ in range(population)]

# gene_space: all the values that the gene can have in the chromosome
gene_space = [people for week in currentCalendar 
                            for dayPos, dayMonth in enumerate(week) 
                                if dayMonth != 0
                                    for dayOfWeek, tasks in tasksDict.items() 
                                        if dayPos == dayOfWeek
                                            for _ in tasks]
# RANDOM SEED SO IT GENERATES DIFFERENT SOLUTIONS EVERYTIME
t = 1000 * time.time() # current time in milliseconds
random.seed(int(t) % 2**32)

# Change fitness function to use tensorflow and make use of the GPU
# Modulate sub-fitness, if it does not affect to the Computational time.

def fitness_func(self, solution, solution_idx):
        
    peopleCountList = []
    freeDaysFitness = 0

    peopleTasks = {}
    peopleIndexTasks = {} # fit 5
    for index, gene in enumerate(solution):
        # Fitness 1. If a person has to complete a task on a free day, the fitness is reduced radically
        freeDaysFitness += evaluateFreeDays(calendarStarts, tasksLenght, index, gene, len(solution))
        
        # Fitness 4.
        # We are obtaining a dictionary that contains each of the different tasks that each of the people have assigned
        if gene not in peopleTasks.keys():
            peopleTasks[gene] = []
        peopleTasks[gene].append(getTaskByIndex(currentCalendar, tasksLenght, tasksDict, index))
    
        # Fit 2. Every person must do more or less the same num of tasks as others
        peopleCountList.append(gene)

        # Fit 5. gather the index of each task to later on see the distance between them 
        if gene not in peopleIndexTasks.keys():
            peopleIndexTasks[gene] = []
        peopleIndexTasks[gene].append(index)

    
    # Fit 2. 
    peopleCount = {person: peopleCountList.count(person) for person in peopleCountList}
    averageTasks = round(len(solution)/len(people))
    tasksPerPersonFitness = 0
    peopleDistancesFitness = 0
    epsilon = 0.1
    
    # Fit 4. For each person benefit how different are the tasks in between each others
    taskDiffCountFitness = 0


    maxPeopleDistribution = math.sqrt(len(people)) * int(averageTasks) * len(solution)/averageTasks

    for person in people:
        # Fit 2
        if person in peopleCount.keys():
            if averageTasks - epsilon <= peopleCount[person] <= averageTasks + epsilon:
                tasksPerPersonFitness += peopleCount[person]/len(solution)
            else:
                tasksPerPersonFitness -= abs(peopleCount[person] - averageTasks)**2/len(solution)
        else: # If that person is not participating then is doing 0 tasks
            tasksPerPersonFitness -= averageTasks**2/len(solution)
        ## Fit 5. Distribution of the task of one person are expanded
        distribution = 0
        if person in peopleIndexTasks.keys():
            for i in range(len(peopleIndexTasks[person])-1, 0, -1):
                distribution += math.sqrt(peopleIndexTasks[person][i] - peopleIndexTasks[person][i-1])
            peopleDistancesFitness += distribution/maxPeopleDistribution

        if person in peopleTasks.keys():
            repTasks = int(round(len(peopleTasks[person])/diffTask, 0))
            if repTasks == 0:
                repTasks += 1
            peopleTasksCounter = Counter(peopleTasks[person])
            for taskicount in peopleTasksCounter.values():
                if taskicount <= repTasks:
                    taskDiffCountFitness += taskicount/len(solution)
                else:
                    taskDiffCountFitness -= taskicount/len(solution)
    
    # Fit 5. 
    tasksInSameDayFitness = 0
        
    # 3. If a person works two times in a day the fitness is reduced radically
    taskCount = 0
    for week in range(len(currentCalendar)):
        for day in range(7):   
            peopleTasksInDay = []
            peopleTasksInDaySet = set()
            for _ in range(taskPerDay[day]):
                if currentCalendar[week][day] != 0:
                    peopleTasksInDay.append(solution[taskCount])
                    peopleTasksInDaySet = set(peopleTasksInDay)
                    taskCount += 1

            if peopleTasksInDaySet:
                repetitionCount = np.array([peopleTasksInDay.count(person) for person in peopleTasksInDaySet])  # One Person doing the same task
                for repetitions in repetitionCount:
                    if repetitions > 1: # if there are repetions
                        tasksInSameDayFitness -= repetitions/len(solution)
                    else:

                        tasksInSameDayFitness += repetitions/len(solution)

    # 1. 
    fitness1 = freeDaysFitness

    # 2. 
    fitness2 = tasksPerPersonFitness
    
    # 3. 
    fitness3 = tasksInSameDayFitness

    # 4.
    fitness4 = taskDiffCountFitness

    ## 5. 
    fitness5 = peopleDistancesFitness


    # Chromosome fitness will be a weighted combination of all scores 
    return fitness1 * alpha1 + fitness2 * alpha2 + fitness3 * alpha3 + fitness4 * alpha4 + fitness5 * alpha5


num_generations = 1000
num_parents_mating = 1
sol_per_pop = 200
num_genes = len(initial_population)

# start = time.time()
# with tf.device('/CPU:0'):
#     ga_instance = pygad.GA(num_generations=num_generations,
#                         num_parents_mating=num_parents_mating,
#                         initial_population=initial_population,
#                         fitness_func=fitness_func,
#                         sol_per_pop=sol_per_pop,
#                         gene_space=gene_space,
#                         num_genes=num_genes)

#     ga_instance.run()
# end = time.time() - start
# print("time with CPU: ", end, "Results: ", ga_instance.best_solution())
# ga_instance.plot_fitness()
# ga_instance.plot_genes()
# ga_instance.plot_new_solution_rate()

start = time.time()
with tf.device('/GPU:0'):
    ga_instance = pygad.GA(num_generations=num_generations,
                        num_parents_mating=num_parents_mating,
                        initial_population=initial_population,
                        fitness_func=fitness_func,
                        sol_per_pop=sol_per_pop,
                        gene_space=gene_space,
                        num_genes=num_genes)

    ga_instance.run()
end = time.time() - start
print("time with GPU: ", end, "Results: ", ga_instance.best_solution())
ga_instance.plot_fitness()
ga_instance.plot_genes()
ga_instance.plot_new_solution_rate()