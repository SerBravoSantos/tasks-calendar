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

"""In this file, we have the class Chromosome and GA 
"""

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
    """This class contains the attributes and methods needed for the chromosome.
    
    Attributes:
        calendar (list[list[int]]): Contains all weeks and days of the month for which we want a tasks calendar. 
        tasksDict (dict[int, list[int]]): Contains the planification of the tasks we need to make by week.
            Example:
                tasksDict = {MONDAY: [TOB], TUESDAY: [TIB, CBB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[CSB], SATURDAY:[], SUNDAY: [VS]}
        people (list[int]): Contains all the people participating in the task calendar.
        mutationProb (float) = the probability for each gene of the chromosome to mutate (Change the value of the gene).
        info (list[int]) = This contains all the genes of the chromosome in case that we want to train one population we already trained before. 
    """
    def __init__(self, calendar, tasksDict, people, mutationProb=0.05, info=None):
        """Initializes the chromosome to their correspondent value
        
        Attributes:
            calendar (list[list[int]]): Contains all weeks and days of the month for which we want a tasks calendar. 
            tasksDict (dict[int, list[int]]): Contains the planification of the tasks we need to make by week.
                Example:
                    tasksDict = {MONDAY: [TOB], TUESDAY: [TIB, CBB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[CSB], SATURDAY:[], SUNDAY: [VS]}
            people (list[int]): Contains all the people participating in the task calendar.
            mutationProb (float) = the probability for each gene of the chromosome to mutate (Change the value of the gene).
            info (list[int]) = This contains all the genes of the chromosome in case that we want to train one population we already trained before
        """
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
        # If we want to retrained a chromosome we just assign the info, if not, we randomly create the gene
        if info:
            self.info = info
            self.population = list(set(self.info))
        else:
            random.seed(15)
            self.info = [random.choice(list(people)) for week in calendar 
                                                        for dayPos, dayMonth in enumerate(week) 
                                                            if dayMonth != 0
                                                                for dayOfWeek, tasks in tasksDict.items() 
                                                                    if dayPos == dayOfWeek
                                                                        for _ in tasks]
            self.population = list(set(self.info))
            t = 1000 * time.time()
            random.seed(int(t) % 2**32)
        
        self.fitness = 0
        self.mutationProb = mutationProb

    def __str__(self):
        """Returns the string of a chromosome

        Returns:
            str: string of the list that represents the genes of the chromosome
        """
        return str(self.info)  

    def evaluate(self):
        """Evaluates the fitness of the chromosome by adding the score of 5 aspects we want to take into account for the calendar
            
            Modifies:
                self.fitness1: The fitness of the chromosome will be affected negatively if a person is assigned to a certain task in a day that he is off.
                self.fitness2: All the people have more or less the same number of tasks.
                self.fitness3: People should not do more than one tasks each day as long as this is possible.
                self.fitness4: People should have different tasks.
                self.fitness5: The tasks of a person should be as much spreaded in time as possible. 
                self.fitness: The final score that combines all the fitnesses in one. 
        """
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

        """
        Fit 5: 
        We need to calculate the maximum distance between tasks, which has to be the number of people
            - dist_max_between_tasks = len(self.people)
        For getting the perfect distribution we need to add n-1 times the ideal distance for all the people
        The number of times we need to multiply the distance is equal to the number of people in the calendar.
        This is because in the perfect scenario, one person will have to do a tasks every cicle where everyone has being assigned a task. 
        Since we meassure the distance between the nearest 2 tasks, we do not count this distance for the first tasks, so we will substract 1 from n_times
            - n_times_ = len(self.people) - 1
        Then, in a calendar we will have to multiply that distance by the number of tasks for the evaluated person, without counting the first task. 
            - ideal_distribution_person = avg_task * n_times_
                where 
            - avg_task = len(self.info)/len(self.people)
        Now, we only need to multiply this ideal distribution per person by the number of people in the calendar. 
            - maxPeopleDistribution = (len(self.people) * n_times_) * math.sqrt(avg_tasks) 
                                    = (len(self.people) * (len(self.people) - 1)) * math.sqrt(avg_tasks)
        """
        avg_tasks = len(self.info)/len(self.people)
        maxPeopleDistribution = (len(self.people) * (len(self.people) - 1)) * math.sqrt(avg_tasks)
        
        
        for person in self.people:
            # Fit 2
            if person in peopleCount.keys():
                if averageTasks_rounded - epsilon <= peopleCount[person] <= averageTasks_rounded + epsilon:
                    tasksPerPersonFitness += peopleCount[person]/len(self.info)
                else:
                    tasksPerPersonFitness -= abs(peopleCount[person] - averageTasks_rounded)**2/len(self.info)
            else: # If that person is not participating then is doing 0 tasks
                tasksPerPersonFitness -= averageTasks_rounded**2/len(self.info)
            """
            Fit 5. Distribution of the task of one person are expanded
            Searching for the possible cases I came with one in which we could have the same results for different combinations that are not equaly good for the calendar. Lets take a calendar with 9 tasks and 3 people (A,B,C). 
            Then lets take this 2 examples:
                - A B C A B C A B C -> A = 3 + 3, B = 3 + 3, C = 3 + 3 -> This, as we can see, should give us the perfect score since here the maxPeopleDistribution is 9 * 2 = 18, so 18/18 = 1. 
                - A B A C B C A B C -> A = 2 + 4, B = 3 + 3, C = 2 + 4 -> This will also give us the same result as the one before (1), but we see that the first solution is going to be more distributed. 
            As a solution, I will sqrt the distance between tasks, so then, our first solution will be better always, now our max distribution will be (len(self.people)**2-len(self.people)) * math.sqrt(avg_tasks) = (9-3)*3**1/2  
                - 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 + 3**1/2 = 10.39 / 10.39 = 1
                - 2**1/2 + 4**1/2 + 3**1/2 + 3**1/2 + 2**1/2 + 4**1/2 = 3.46 + 2.82 + 4 / 12.72 = 10.28 / 10.39 = 0.989
            """
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
                peopleTasksInDaySet = {}
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

        self.fitness1 = freeDaysFitness
        self.fitness2 = tasksPerPersonFitness
        self.fitness3 = tasksInSameDayFitness
        self.fitness4 = taskDiffCountFitness
        self.fitness5 = peopleDistancesFitness
        self.fitness = self.fitness1 * alpha1 + self.fitness2 * alpha2 + self.fitness3 * alpha3 + self.fitness4 * alpha4 + self.fitness5 * alpha5

    def updatePeople(self):
        """Updates the array of people of the chromosome 
        """
        self.population = list(set(self.info))
        
    # Mutation Funtion for the chromosome
    def mutateChromosome(self, typeMutation = RANDOM_MUTATION_PEOPLE_PROP):
        """Function that mutates the chromosome. 
        
        Args:
            typeMutation (int): enumerate that indicates the type of mutation
        
        There are different types of mutation:
            RANDOM_MUTATION: Changes the gen with any of the other people in the pool.
            RANDOM_MUTATION_PEOPLE_NOT_IN: Changes the gen with any of the other people in the pool, but if any of the people is not participating in the calendar it will first take from this pool.
            RANDOM_MUTATION_PEOPLE_PROP: It establishes a probability for each person depending on how much do they appear in the calendar. The less they appear in the calendar, the better the probability of being chosen. 
        """
        # We create a copy of the chromosome which will be the child (As we modify it)
        chromosomeChild = copy.deepcopy(self)    

        if typeMutation == RANDOM_MUTATION:
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,100)/100:
                    choices = [person for person in self.population if info != person]
                    chromosomeChild.info[i] = random.choice(choices)
        elif typeMutation == RANDOM_MUTATION_PEOPLE_NOT_IN:
            peopleNotIn = set([person for person in self.population if not person in self.info])
            if not peopleNotIn:
                peopleNotIn = self.population
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,10)/10:
                    choices = [person for person in peopleNotIn if info != person]
                    chromosomeChild.info[i] = random.choice(choices)
        elif typeMutation == RANDOM_MUTATION_PEOPLE_PROP:
            probPeople = {person: 1 for person in self.population}
            for person in self.population:
                for personGen in self.info:
                    if person == personGen:
                        probPeople[person] += 1
            probPeopleInv = np.array([1/prob for prob in probPeople.values()])
            probPeopleInv = probPeopleInv/sum(probPeopleInv)
            for i, info in enumerate(self.info):
                if self.mutationProb >= random.randint(0,10)/100:
                    chromosomeChild.info[i] = choice(self.population, 1, p=probPeopleInv)[0]
                    
        self.updatePeople()
        return chromosomeChild
            

class GA:
    """This class contains the attributes and methods needed for the genetic algorithm.
    
    Attributes:
        calendar (list[list[int]]): Contains all weeks and days of the month for which we want a tasks calendar. 
        tasksDict (dict[str, list[str]]): Contains the planification of the tasks we need to make by week.
            Example:
                tasksDict = {MONDAY: [TOB], TUESDAY: [TIB, CBB],  WEDNESDAY: [CBB], THURSDAY:[CK], FRIDAY:[CSB], SATURDAY:[], SUNDAY: [VS]}
        people (list[int]): Contains all the people participating in the task calendar.
        sizePopulation (int): size of the Population.
        mutationGeneProb (float) = the probability for each gene of the chromosome to mutate (Change the value of the gene).
        typeSelection (int) = defines the type of selection we want for our algorithm.
        typeMutation (int) = defines the type of mutation we want for our algorithm.
        typeCrossover (int) = defines the type of crossover function we want for our algorithm.
        mutationProb (float) = Probability of mutating the chromosome evaluated.
        kpoints = Number of elbows we want for the KPOINT crossover.
        uniformCross = the probability of swapping the genes. 
        load = True if we want to load the population.
        early_stop = if setted, defines the number of iterations the algorithm does without having a better individual before stopping. None, if we do not want early stopping 
    """
    def __init__(self, calendar, tasksDict, people, sizePopulation, mutationGeneProb=0.05, typeSelection = ROULETTE, 
                    typeMutation = RANDOM_MUTATION_PEOPLE_PROP, typeCrossover = UNIFORMCROSSOVER, 
                        mutationProb = 0.5, kpoints=3, uniformCross = 0.5, load=False, earlyStop = None):
        """Initializes the GA.
        """
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
        """Returns the string of the GA.

        Returns:
            str: Returns the number of chromosomes of the population.
        """
        return "Population of: {}".format(self.sizePopulation)

    def trainGA(self, iterations=20):
        """trains the GA

        Args:
            iterations (int): number of iterations for the training. Defaults to 20.
        """
        def writeFitnessFiles(iteration):
            """write all the files for the experiments.

            Args:
                iteration (int): the number of iteration. 
            """
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

        # Start of the algorithm 
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
        
            # Breaks if the fitness of the actual popularion is not stricktly higher than the fitness of the best solution for x iterations
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
        """Evaluate the population by calling each evaluation method for each chromosome.

        Returns:
            scores list[float]: The scores for each chromosome of the population.
        """
        scores = [] 
        for chromosome in self.population:
            chromosome.evaluate()
            scores.append(chromosome.fitness)
        return scores

    def selection(self):
        """Obtains the new population based on the last population.
        The roulette method consists on selecting the individuals based on the fitness score they have. 
        The probability is the actual score of the chromosome / total score.

        Returns:
            scores list[float]: The scores for each chromosome of the population.
        """
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
        """Mutate each chromosome (if chosen randomly) using the chromosome mutating method.
        
            Changes:
                self.population
        """
        childs = []
        for chromosome in self.population:
            if self.mutationProb >= random.randint(0,10)/10:
                childs += [chromosome.mutateChromosome(self.typeMutation)]
            else:
                childs += [chromosome]
        self.population = childs

    def crossPopulation(self, chrom1, chrom2):
        """This function will cross the chromosomes by pairs to obtain new chromosomes. 
            There are 2 types:
            - k points crossover: Takes k random points of the chromosome and exchanges alternatively the chain of genes from one point to the following. 
            - uniform crossover: Swaps each gene individually based on a probability of being swapped.
        
            Returns:
                The 2 copies of the chomosome.
        """
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
        """Loads the past population file and assign it to the population of the GA instance.
        """
        with open(bestGensSavePath, "r") as f:
            lines = f.readlines()
        return [Chromosome(calendar, tasksDict, people, mutationProb ,[int(gene) for gene in line.strip("\n").split(",")[:-1]]) for line in lines]
        