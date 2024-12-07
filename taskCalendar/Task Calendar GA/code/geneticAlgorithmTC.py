import numpy as np
from collections import Counter
import random
import copy 
from numpy.random import choice
import os
from config import *
import math
from calendarFunctions import *
import time

# Falta Weighted Tasks Fitness 6
# Falta Pensar prioridad de tareas? (Separar BINS de las demás tareas)
# Limpiar Código
# Modular + poco Acoplamiento
codePath = os.path.dirname(os.path.realpath(__file__))
dirPath = os.path.abspath(os.path.join(codePath, os.pardir))
dataPath = os.path.join(dirPath, "data")
textfilesPath = os.path.join(dataPath, "textFiles")
savefilesPath = os.path.join(dataPath, "save")
bestGensPath = os.path.join(textfilesPath, "bestGenerations.txt")
bestGensSavePath = os.path.join(savefilesPath, "bestGene.txt")
fit1Path = os.path.join(textfilesPath, "bestFit1.txt")
fit2Path = os.path.join(textfilesPath, "bestFit2.txt")
fit3Path = os.path.join(textfilesPath, "bestFit3.txt")
fit4Path = os.path.join(textfilesPath, "bestFit4.txt")
fit5Path = os.path.join(textfilesPath, "bestFit5.txt")

class Chromosome:

    def __init__(self, calendar, tasksDict, people, mutationProb=0.05, info=None):
        self.calendar = calendar
        self.nTasks = sum([len(tasks) for tasks in list(tasksDict.values())])
        self.diffTask = len(set([val for values in tasksDict.values() for val in values]))
        self.taskPerDay = list([len(tasks) for tasks in list(tasksDict.values())])
        
        count = 0
        for day in calendar[0]:
            if day != 0:
                self.dayStart = count
            count += 1

        self.tasksDict = tasksDict
        self.people = people
        # First create array for the tasks
        if info:
            self.info = info
        else:
            random.seed(15)
            self.info = [random.choice(list(people)) for week in calendar 
                                        for dayPos, dayMonth in enumerate(week) 
                                            if dayMonth != 0
                                                for dayOfWeek, tasks in tasksDict.items() 
                                                    if dayPos == dayOfWeek
                                                        for _ in tasks]
            t = 1000 * time.time() # current time in milliseconds
            random.seed(int(t) % 2**32)
        
        self.fitness = 0
        self.mutationProb = mutationProb

    def __str__(self):
        return str(self.info)  

    
    # Sets the fitness of the chromosome by evaluating it
    def evaluate(self):
            
        peopleCountList = []
        freeDaysFitness = 0

        peopleTasks = {}
        peopleIndexTasks = {} # fit 5
        for index, gene in enumerate(self.info):
            # Fitness 1. If a person has to complete a task on a free day, the fitness is reduced radically
            freeDaysFitness += evaluateFreeDays(self, index, gene, len(self.info))
            
            # Fitness 4.
            # We are obtaining a dictionary that contains each of the different tasks that each of the people have assigned
            if gene not in peopleTasks.keys():
                peopleTasks[gene] = []
            peopleTasks[gene].append(getTaskByIndex(self, self.tasksDict, index))
          
            # Fit 2. Every person must do more or less the same num of tasks as others
            peopleCountList.append(gene)

            # Fit 5. gather the index of each task to later on see the distance between them 
            if gene not in peopleIndexTasks.keys():
                peopleIndexTasks[gene] = []
            peopleIndexTasks[gene].append(index)

        
        # Fit 2. 
        peopleCount = {person: peopleCountList.count(person) for person in peopleCountList}
        averageTasks_rounded = round(len(self.info)/len(self.people))
        tasksPerPersonFitness = 0
        peopleDistancesFitness = 0
        epsilon = 0.1
        
        # Fit 4. For each person benefit how different are the tasks in between each others
        taskDiffCountFitness = 0

        # Fit 5: 
        # Antiguo 
        # maxPeopleDistribution = math.sqrt(len(self.people)) * int(averageTasks_rounded) * len(self.info)/averageTasks_rounded
        
        # We need to calculate the maximum distance between tasks, which has to be the number of people
            # dist_max_between_tasks = len(self.people)
        avg_tasks = len(self.info)/len(self.people)
        # For getting the perfect distribution we need to add n-1 times the ideal distance for all the people
        # The number of times we need to multiply the distance is equal to the number of people in the calendar.
        # This is because in the perfect scenario, one person will have to do a tasks every cicle where everyone has being assigned a task. 
        # Since we meassure the distance between the nearest 2 tasks, we do not count this distance for the first tasks, so we will substract 1 from n_times
        # n_times_ = len(self.people) - 1
        # Then, in a calendar we will have to multiply that distance by the number of tasks for the evaluated person, without counting the first task. 
        # ideal_distribution_person = avg_task * n_times_
        # where 
        # avg_task = len(self.info)/len(self.people)
        # Now, we only need to multiply this ideal distribution per person by the number of people in the calendar. 
        # maxPeopleDistribution = (len(self.people) * n_times_) * math.sqrt(avg_tasks) = (len(self.people) * (len(self.people) - 1)) * math.sqrt(avg_tasks-1)
        
       
        
        maxPeopleDistribution = (len(self.people) * (len(self.people) - 1)) * math.sqrt(avg_tasks-1)
        
        
        for person in self.people:
            # Fit 2
            if person in peopleCount.keys():
                if averageTasks_rounded - epsilon <= peopleCount[person] <= averageTasks_rounded + epsilon:
                    tasksPerPersonFitness += peopleCount[person]/len(self.info)
                else:
                    tasksPerPersonFitness -= abs(peopleCount[person] - averageTasks_rounded)**2/len(self.info)
            else: # If that person is not participating then is doing 0 tasks
                tasksPerPersonFitness -= averageTasks_rounded**2/len(self.info)
            ## Fit 5. Distribution of the task of one person are expanded
            # Searching for the possible cases I came with one in which we could have the same results for different combinations that are not equaly good for the calendar. Lets take a calendar with 9 tasks and 3 people (A,B,C). 
            # Then lets take this 2 examples:
            # A B C A B C A B C -> A = 3 + 3, B = 3 + 3, C = 3 + 3 -> This, as we can see, should give us the perfect score since here the maxPeopleDistribution is 9 * 2 = 18, so 18/18 = 1. 
            # A B A C B C A B C -> A = 2 + 4, B = 3 + 3, C = 2 + 4 -> This will also give us the same result as the one before (1), but we see that the first solution is going to be more distributed. 
            # As a solution, I will sqrt the distance between tasks, so then, our first solution will be better always, now our max distribution will be (len(self.people)**2-len(self.people)) * math.sqrt(avg_tasks) = (9-3)*3**1/2  
            # 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 = 10.39 / 10.39 = 1
            # 2**1/2 + 4**1/2 + 3**1/2 + 3**1/2 + 2**1/2 + 4**1/2 = 3.46 + 2.82 + 4 / 12.72 = 10.28 / 10.39 = 0.989
            distribution = 0
            if person in peopleIndexTasks.keys():
                for i in range(len(peopleIndexTasks[person])-1, 0, -1):
                    distribution += math.sqrt(peopleIndexTasks[person][i] - peopleIndexTasks[person][i-1])
                peopleDistancesFitness += distribution/maxPeopleDistribution

            if person in peopleTasks.keys():
                repTasks = int(round(len(peopleTasks[person])/self.diffTask, 0))
                if repTasks == 0:
                    repTasks == 1
                peopleTasksCounter = Counter(peopleTasks[person])
                for taskicount in peopleTasksCounter.values():
                    if taskicount <= repTasks:
                        taskDiffCountFitness += taskicount/len(self.info)
                    else:
                        taskDiffCountFitness -= taskicount/len(self.info)
        
        # Fit 5. 
        tasksInSameDayFitness = 0
            
        # 3. If a person works two times in a day the fitness is reduced radically
        taskCount = 0
        for week in range(len(self.calendar)):
            for day in range(7):   
                peopleTasksInDay = []
                peopleTasksInDaySet = set()
                for _ in range(self.taskPerDay[day]):
                    if self.calendar[week][day] != 0:
                        peopleTasksInDay.append(self.info[taskCount])
                        peopleTasksInDaySet = set(peopleTasksInDay)
                        taskCount += 1

                if peopleTasksInDaySet:
                    repetitionCount = np.array([peopleTasksInDay.count(person) for person in peopleTasksInDaySet])  # One Person doing the same task
                    for repetitions in repetitionCount:
                        if repetitions > 1: # if there are repetions
                            tasksInSameDayFitness -= repetitions/len(self.info)
                        else:

                            tasksInSameDayFitness += repetitions/len(self.info)

        # 1. 
        self.fitness1 = freeDaysFitness

        # 2. 
        self.fitness2 = tasksPerPersonFitness
        
        # 3. 
        self.fitness3 = tasksInSameDayFitness

    	# 4.
        self.fitness4 = taskDiffCountFitness

        ## 5. 
        self.fitness5 = peopleDistancesFitness


        # Chromosome fitness will be a weighted combination of all scores 
        self.fitness = self.fitness1 * alpha1 + self.fitness2 * alpha2 + self.fitness3 * alpha3 + self.fitness4 * alpha4 + self.fitness5 * alpha5

    # Updates the array of people of the chromosome
    def updatePeople(self):
        self.people = list(set(self.info))
        
    # Mutation Funtion for the chromosome
    def mutateChromosome(self, typeMutation = RANDOM_MUTATION_PEOPLE_PROP):
        
        # We create a copy of the chromosome which will be the child (As we modify it)
        chromosomeChild = copy.deepcopy(self)    

        if typeMutation == RANDOM_MUTATION:
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,10)/10:
                    choices = [person for person in self.people if info != person]
                    chromosomeChild.info[i] = random.choice(choices)

        elif typeMutation == RANDOM_MUTATION_PEOPLE_NOT_IN:
            peopleNotIn = set([person for person in self.people if not person in self.info])
            if not peopleNotIn:
                peopleNotIn = self.people
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,10)/10:
                    choices = [person for person in peopleNotIn if info != person]
                    chromosomeChild.info[i] = random.choice(choices)

        elif typeMutation == RANDOM_MUTATION_PEOPLE_PROP:
            probPeople = {person: 1 for person in self.people}
            for person in self.people:
                for personGen in self.info:
                    if person == personGen:
                        probPeople[person] += 1
            probPeopleInv = np.array([1/prob for prob in probPeople.values()])
            probPeopleInv = probPeopleInv/sum(probPeopleInv)
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,10)/100:
                    chromosomeChild.info[i] = choice(self.people, 1, p=probPeopleInv)[0]
                    

        self.updatePeople()

        return chromosomeChild
            

class GA:

    def __init__(self, calendar, tasksDict, people, sizePopulation, mutationGeneProb=0.05, typeSelection = ROULETTE, 
                    typeMutation = RANDOM_MUTATION_PEOPLE_PROP, typeCrossover = UNIFORMCROSSOVER, 
                        mutationProb = 0.5, kpoints=3, uniformCross = 0.5, load=False, earlyStop = None):
        self.sizePopulation = sizePopulation
        self.typeSelection = typeSelection
        self.typeMutation = typeMutation
        self.typeCrossover = typeCrossover
        self.mutationProb = mutationProb
        self.kpoints = kpoints
        self.uniformCross = uniformCross
        self.earlyStop = earlyStop
        if load:
            print("\nloading from file\n")
            self.population = self.loadChromoFile(bestGensSavePath, calendar, tasksDict, people, mutationProb)
        else:
            self.population = [Chromosome(calendar, tasksDict, people, mutationGeneProb) for i in range(sizePopulation)]

        self.scores = self.evaluate()
        indBest = np.argmax(self.scores)
        self.best = self.population[indBest]
        
    def __str__(self):
        return "Population of: {}".format(self.sizePopulation)

    def trainGA(self, iterations=20):

        def writeFitnessFiles(iteration):
            if iteration == 0:
                with open(bestGensPath, "w+") as f:
                    f.write("it\t\tinfo\t\tfitness\n")
                    f.write("{}\t\t{}\t\t{}\n".format(iteration, self.population[indBest].info, self.population[indBest].fitness))
                with open(fit1Path, "w+") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness1))
                with open(fit2Path, "w+") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness2))
                with open(fit3Path, "w+") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness3))
                with open(fit4Path, "w+") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness4))
                with open(fit5Path, "w+") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness5))
            # Compare last best with new best
            if self.population[indBest].fitness > self.best.fitness:
                with open(bestGensPath, "a") as f:
                    f.write("{}\t\t{}\t\t{}\n".format(iteration, self.population[indBest].info, self.population[indBest].fitness))
                with open(fit1Path, "a") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness1))
                with open(fit2Path, "a") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness2))
                with open(fit3Path, "a") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness3))
                with open(fit4Path, "a") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness4))
                with open(fit5Path, "a") as f:
                    f.write("{}\t\t{}\n".format(iteration, self.population[indBest].fitness5))

                # Save best population for reset
                with open(bestGensSavePath, "w+") as f:
                    for chromosome in self.population:
                        for gene in chromosome.info:
                            f.write("{},".format(gene))
                        f.write("\n")

        bestScores = []
        bestScores1 = []
        bestScores2 = []
        bestScores3 = []
        bestScores4 = []
        bestScores5 = []

        bestLastIteration = 0
        for iteration in range(iterations):
            
            # Evaluate
            self.scores = self.evaluate()
            
            # Get Best chromosome
            indBest = np.argmax(self.scores)

            # Write fitness into files
            writeFitnessFiles(iteration)
        
            if self.earlyStop:
                if bestLastIteration >= self.earlyStop:
                    break                
                if self.population[indBest].fitness > self.best.fitness:
                    bestLastIteration = 0
                else:
                    bestLastIteration += 1

            self.best = self.population[indBest]
            bestScores.append(self.best.fitness)
            bestScores1.append(self.best.fitness1)
            bestScores2.append(self.best.fitness2)
            bestScores3.append(self.best.fitness3)
            bestScores4.append(self.best.fitness4)
            bestScores5.append(self.best.fitness5)

            print("iteration: {} Best generation Score: {}".format(iteration, self.best.fitness))
        
            # Selection
            self.sortIndexScores = np.argsort(self.scores)[::-1]
            newPopulation = self.selection()
            covPopulation = []

            # Cross Population
            for i in range(0,len(newPopulation)-1,2):
                if i+2 <= len(newPopulation)-1:
                    child1, child2 = self.crossPopulation(newPopulation[i], newPopulation[i+1])
                    covPopulation += [child1, child2]
                else:
                    covPopulation += [newPopulation[i+1]]
            self.population = covPopulation 
            
            # Mutation 
            self.mutatePopulation()
            self.population += [newPopulation[-1]] # We add the best child
        return [bestScores, bestScores1, bestScores2, bestScores3, bestScores4, bestScores5]

    def evaluate(self):
        scores = [] 
        for chromosome in self.population:
            chromosome.evaluate()
            scores.append(chromosome.fitness)
        return scores

    def selection(self):
        newChromosomes = []
        epsilon = 0.00000000001
        if self.typeSelection == ROULETTE:
            sumScores = sum(self.scores) + epsilon
            probSelection = []
            probSelected = 0
            for indChrom in self.sortIndexScores:
                probSelected += self.scores[indChrom]/sumScores
                probSelection.append(probSelected)
            probSelection[-1] = 1
            probs = list(map(lambda _: random.randint(0,100)/100, range(self.sizePopulation-1))) # Best remains
            for prob in probs:
                rangeAssigned = False
                for i, threshold in enumerate(probSelection):
                    if prob <= threshold and not rangeAssigned:
                        newChromosomes.append(self.population[i])
                        rangeAssigned = True
        newChromosomes.append(self.best)
        return newChromosomes

    def mutatePopulation(self):

        childs = []
        for chromosome in self.population:
            if self.mutationProb >= random.randint(0,10)/10:
                childs += [chromosome.mutateChromosome(self.typeMutation)]
            else:
                childs += [chromosome]
        self.population = childs

    # Cross chromosomes Function
    def crossPopulation(self, chrom1, chrom2):
        child1, child2 = copy.deepcopy(chrom1), copy.deepcopy(chrom2)
        if self.typeCrossover == KPOINT:
            crosspointsChoices = list(range(len(chrom1.info)))
            crosspoints = random.sample(crosspointsChoices, self.kpoints)
            crosspoints.sort()
            i = 0
            swap = True
            for cp in crosspoints:
                if swap:
                    child1.info[i:cp] = chrom2.info[i:cp]
                    child2.info[i:cp] = chrom1.info[i:cp]
                    swap = False
                else:
                    swap = True
                i=cp
        elif self.typeCrossover == UNIFORMCROSSOVER:
            for i in range(len(chrom1.info)):
                if self.uniformCross >= random.randint(0, 10)/10:
                    child1.info[i] = chrom2.info[i]
                    child2.info[i] = chrom1.info[i]
        return child1, child2

    def loadChromoFile(self, bestGensSavePath, calendar, tasksDict, people, mutationProb):
        with open(bestGensSavePath, "r") as f:
            lines = f.readlines()
        return [Chromosome(calendar, tasksDict, people, mutationProb ,[int(gene) for gene in line.strip("\n").split(",")[:-1]]) for line in lines]
        