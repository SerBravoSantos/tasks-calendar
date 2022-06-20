# Tasks Calendar



## Index
1. **[Introduction](#Introduction)**
2. **[Development](#Development)**
    1. **[Calendar](#Calendar)**
    2. **[Gene](#Gene)**
    3. **[Evaluation](#Evaluation)**
    4. **[Selection](#Selection)**
    5. **[Mutation](#Mutation)**
    6. **[Crossover](#Crossover)**
    7. **[Callbacks](#Callbacks)**
    8. **[Plots and Visualization](#Plots-and-Visualization)**
4. **[Hiper-Parameters Selection](#Hiper-Parameters-Selection)**
5. **[Results](#Results)**
6. **[Conclusions](#Conclusions)**
7. **[Future Ideas](#Future-Ideas)**
8. **[Usage Guide](#Usage-Guide)**

## Introduction

For me, coming to Dublin (Ireland) has becomed an opportunity for discovering new places to visit, different tastes to try, people that introduced me to their cultures and that I shared really good moments with and lots more...
As you can see, living abroad can open you a wide range of novel experiences that can frighten anyone but at the end it will make you learn and grow personally, as you enjoy the path. 

Nevertheless, and here is where I tell you what this page is created for, I had as many good occurrences, as bad ones. 
In specific, in this page we will talk about the really hard aspect of living with more people in(at?) the same house, and this aspect is the organization for doing all the common duties needed in order to keep the common areas of the house cleaned and enjoyable for living. 

Since I came to this house, about 8 months ago, the method used for the cleanse of the common spaces have been a handmade task calendar that contained a fixed structure of different tasks spreaded over the month, and the different housemates assigned for each of the task. This is a great idea, but I was lazy to create my calendar, and this is the reason why I started developing this project!

## Model Selection 

Before starting developing the whole idea, there were some issues to take care of first. 

First, the problem needs to be defined. 

In this case, we will have a calendar with fixed tasks, so the people always know when the task are due to do. Then, we will have an array of people which will be assigned for each of the tasks. The goal of the model will be assigning the best spot possible for each of the housemates. Not as easy as it seems, this goal will be depending on the rules we want to impose. 

We can now discart supervised learning, we do not have a dataset that we can show to the model to learn how to predict the correct output. 

But unsupervised learning fits well in the definition of the problem as we do not have collected data, but we do have a set of states (Each possibie combination of people assigned to the tasks in a period of time), a set of actions (this actions could be assiging a certain task to a different person for example) and goal (which in this case it will be having the best possible configuration founded).

Having this information, I decided to implement a genetic algorithm for different reasons:
- I already used this algorithm in one past project in the university, so I can use everything I learned into accomplish the objectives.
- Even though its simplicity, it gets good results and nowadays people still use this solution for solving many problems.
- GAs are pretty flexible at the time of customizing the algorithm to get different results deppending on the problem. 

## Genetic Algorithm

The genetic algorithm (GA) is an heuristic search, we could consider it as an stochastic variant of the local beam search, which uses multiple states that search for the goal simultaneously. 
This variant is inspired in Charles Darwin's natural evolution theory, the way we obtain all the successors for the next generation is by crossing their parent states. To clarify, in GAs this multiple states will be referred as chromosomes or individuals, which will have a gene assigned. 

The genetic algorithm has 4 phases in its training process:

1. **Evaluation:** 
    Each of the chromosomes of the total population are evaluated following a criteria previously accepted. This evaluation will tell the algorithm how good is the individual. The criteria chosen will be the fitness function, and the fitness score will determine the quality of the chromosome.
2. **Selection:** 
    After evaluation, the GA chooses the next generation which will be transformed later on using the crossover and mutation functions. There exists different techniques to select the new population. 
3. **Crossover:** 
    The crossover function combines two chromosomes to obtain two different childs.
4. **Mutation:** 
    The mutation function modifies the gene the chromosomes chosen by probability. This modification adds a random factor that sometimes can improve the fitness score of the individual. 

This training process will be repeated several times until we decide. If there is an specific goal, the algorithm can stop once it has reached the goal, in this case there is not an specific goal, so we can set a number of iterations or use other techniques like the early stoping which will stop the training if there is not an improvement in N iterations. 

## Development

In this section, we will see how we addapted the algorithm for this specific problem and discuss the problems that have ocurred in the development process. 

### Calendar
(Calendar library (Link to the library page)
The Python [Calendar Library](https://docs.python.org/3/library/calendar.html) used in this project has functions for getting the calendar that we are going to use for the chromosome structure. In the following example, we are retrieving the calendar by month of the year selected. 
```
YEAR = 2022
MONTH = 7 (July)
calendar = calendar.monthcalendar(YEAR, MONTH)
```

### Gene
The gene for our algorithm will be an array of elements, each possition will correspond to a task and the day of the month, previously initialized. Each of the possition will have a person assigned to do this task. 

#### Example of Gene
```
CTB = Check the bins
CK = Clean the kitchen 

tasks = {MONDAY: [CTB], TUESDAY: [],  WEDNESDAY: [], THURSDAY:[CK], FRIDAY:[], SATURDAY:[], SUNDAY: []}
people = [ALICE, BOB, CHARLIE, DAVID]
calendar = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]]

Gene = [1, 2, 3, 4] # Where each of the people have an integer value assigned
```

In this small sample we will have for each monday in the calendar array, one possition that corresponds to the task CTB, and the other two elements of the gene will correspond to othe thursday task CK. 
   
It is a nice structure since the gene will contain just the neccessary information which are the tasks and the people assigned to it. Since each of the index referes to a certain task that correspond to a certain date in the time, we can easily convert a calendar of task into a gene, and viceversa. 

All of the functions needed for obtaining the day, week and task from the position of the gene are all gathered in the library calendarFunctions.   
   
### Evaluation
This is probably the most problematic function to program in a GA. First, the evaluation will depends on the definition of the project, so you have to provide a function that provides you a fitness score correct. Second, the fitness score evaluated shows how better is one individual versus another, so the algorithm needs to be optimized and tuned as best as possible so the model trains correctly. If the criteria chosen for the fitness score changes, we need to addapt the evaluation method. 

#### Criteria
To evaluate the chromosome I had to collect all the aspects and restrictions I considered that would be neccessary for the task calendar to be optimum.
- People can have holidays in which they will not be able to complete a task.
- The tasks will be equally distributed in between all participants. 
- A person will not have more than one task in a day as long as it is possible.
- The type of tasks of each participant will be as diverse as possible.
- The time in between the tasks of the participants will be as equally distributed as possible. 

Based on this premises, I created 5 different fitness scores for each of them, and combined them in the following equation.

$$ Fitness Score = fit1*\alpha_1 + fit2 \alpha_2 + fit3 \alpha_3 + fit4 \alpha_4 + fit5 \alpha_5 $$

(Criteria)
(Solution)
(Talk about the normalization problem)

#### Selection

(Roulette Method)

#### Mutation

(Mutation Methods) (Include all 3 or maybe avoid the ones that do not work)

### Crossover

(Uniform CrossOver)

(Kpoints CrossOver)

### Callbacks

- Early stopping
- Checkpointing

### Plots and Visualization

Calendar React API (Fullcalendar) - Link

Matplot Lib - Link

### Experimentation

Comparison between (Uniform Crossover and Kpoints)

Comparison Between Mutation Methods

Hiper-Parameters Selection (Mutation Rates, Crossover Rates)

Population 

### Results

With the final configuration, We run the project and we will discuss:

- Fitness Score
- Execution Time
- 

### Conclusions

Talk about the aspects you want to reforce, the ideas, the keypoints of the algorithm, the weak and strong points

### Future Ideas

- Possible Different criterias depending on what someone wants (Adding a description of the weighted tasks). 
- Adjustable parameters for the criteria
- Diversity of calendars (not only one month but one week, two months, one year)...
- Selection of different models (Maybe talk about deep Unsupervised Learning methods like critic actor - Only if you can make an idea of how would it be made)

### Project structure

### Usage Guide

### Reproducing solution
