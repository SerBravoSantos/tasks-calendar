# Tasks Calendar



## Index
1. **[Project Structure](#Project-Structure)**
2. **[Introduction](#Introduction)**
3. **[Model Selection](#Model-Selection)**
4. **[Genetic Algorithm](#Genetic-Algorithm)**
5. **[Development](#Development)**
    1. **[Calendar](#Calendar)**
    2. **[Gene](#Gene)**
    3. **[Evaluation](#Evaluation)**
    4. **[Selection](#Selection)**
    5. **[Crossover](#Crossover)**
    6. **[Mutation](#Mutation)**
    7. **[Callbacks](#Callbacks)**
4. **[Plots and Visualization](#Plots-and-Visualization)**
5. **[Experimentation](#Experimentation)**
    1. **[Crossover Selection](#Crossover-Selection)**
    2. **[Mutation Selection](#Mutation-Selection)**
7. **[Results](#Results)**
8. **[Conclusions](#Conclusions)**
9. **[Future Ideas](#Future-Ideas)**
10. **[Usage Guide](#Usage-Guide)**

 $~~~~~~~~~~~$

## Project structure

The project has the following structure:
- **code/**: This folder contains the files for the model, calendar functions, plots, config and the main file.
- **data/**: This folder contains: 
    - **graphs/**: graphs for the fitness scores of the configuration we want
    - **save/**: Best Chomosome saved genes obtained in the last training.
    - **savedCalendars/**: Calendar screenshots. 
    - **textFiles/**: Best individual fitness scores and execution time for the configuratio wantedn.
    - **calendar.txt**: Best calendar obtained in the last training.

 $~~~~~~~~~~~$

## Introduction

For me, coming to Dublin (Ireland) has becomed an opportunity for discovering new places to visit, different tastes to try, people that introduced me to their cultures and that I shared really good moments with and lots more...
As you can see, living abroad can open you a wide range of novel experiences that can frighten anyone but at the end it will make you learn and grow personally, as you enjoy the path. 

Nevertheless, and here is where I tell you what this page is created for, I had as many good occurrences, as bad ones. 
In specific, in this page we will talk about the really hard aspect of living with more people in the same house, and this aspect is the organization for doing all the common duties needed in order to keep the common areas of the house cleaned and enjoyable for living. 

Since I came to this house, about 8 months ago, the method used for the cleanse of the common spaces have been a handmade task calendar that contained a fixed structure of different tasks spreaded over the month, and the different housemates assigned for each of the task. This is a great idea, but I was lazy to create my calendar, and this is the reason why I started developing this project!

$~~~~~~~~~~~$

## Model Selection 

Before starting developing the whole idea, there were some issues to take care of first. 

First, the problem needs to be defined. 

In this case, we will have a calendar with fixed tasks, so the people always know when the task are due to do. Then, we will have an array of people which will be assigned for each of the tasks. The goal of the model will be assigning the best spot possible for each of the housemates. Not as easy as it seems, this goal will be depending on the rules we want to impose. 

Now, lets think the machine learning approach of the problem, we can discard supervised learning since we do not have a dataset that we can show to the model to learn how to predict the correct output. 

But unsupervised learning fits well in the definition of the problem as we do not have collected data, but we do have a set of states (Each possibie combination of people assigned to the tasks in a period of time), a set of actions (this actions could be assiging a certain task to a different person for example) and a goal (which in this case it will be having the best possible configuration founded).

Having this information, I decided to implement a genetic algorithm for different reasons:
- I already used this algorithm in one past project in the university, so I can use everything I learned into accomplish the objectives.
- Even though its simplicity, it gets good results and nowadays people still use this solution for solving many problems.
- GAs are pretty flexible at the time of customizing the algorithm to get different results deppending on the problem. 

 $~~~~~~~~~~~$

## Genetic Algorithm

The genetic algorithm (GA) is an heuristic search, we could consider it as an stochastic variant of the local beam search, which uses multiple states that search for the goal simultaneously. 
This variant is inspired in Charles Darwin's natural evolution theory, the way we obtain all the successors for the next generation is by crossing their parent states. To clarify, in GAs this multiple states will be referred as chromosomes or individuals, which will have a gene assigned. 

The genetic algorithm has 4 phases in its training process:

1. **Evaluation:** 
    Each of the chromosomes of the total population are evaluated following a criteria previously accepted. This evaluation will tell the algorithm how good is the individual. The criteria chosen will be the fitness function, and the fitness score will determine the quality of the chromosome.
2. **Selection:** 
    After evaluation, the GA chooses the next generation which will be transformed later on using the crossover and mutation functions. Usually, we want to prioritize the selection of better individuals. There exists different techniques to select the new population. 
3. **Crossover:** 
    The crossover function combines two chromosomes to obtain two different childs.
4. **Mutation:** 
    The mutation function modifies the genes of the chromosomes chosen by probability. This modification could add a random factor that sometimes can improve the fitness score of the individual. 

This training process will be repeated several times until we decide. If there is an specific goal, the algorithm can stop once it has reached the goal, in this case there is not an specific goal, so we can set a number of iterations or use other techniques like the early stoping which will stop the training if there is not an improvement in N iterations. 

$~~~~~~~~~~~$

## Development

In this section, we will see how we addapted the algorithm for this specific problem and discuss the problems that have ocurred in the development process. 

### Calendar

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
This is probably the most problematic function to program in a GA. First, the evaluation will depends on the definition of the project, so you have to provide a function that provides you a fitness score correct. Second, the fitness score evaluated shows how better is one individual compared to another, so the algorithm needs to be optimized and tuned as best as possible so the model trains correctly. If the criteria chosen for the fitness score changes, we need to addapt the evaluation method. 

To evaluate the chromosome I had to collect all the aspects and restrictions I considered that would be neccessary for the task calendar to be optimum.
1 People can have holidays in which they will not be able to complete a task.
2 The tasks will be equally distributed in between all participants. 
3 A person will not have more than one task in a day as long as it is possible.
4 The type of tasks of each participant will be as diverse as possible.
5 The time in between the tasks of the participants will be as equally distributed as possible. 

Based on this criteria, I created 5 different fitness scores for each of them, and combined them in the following equation.

$$ Total Fitness Score = fit1\alpha_1 + fit2\alpha_2 + fit3\alpha_3 + fit4\alpha_4 + fit5\alpha_5 $$

$\alpha$ is the multiplier that will adjust the formula depending on the priority we want to have for each rule.

The combination of all of the scores into a final one was tedious for several reasons. 

On one hand, we have to decide $\alpha$ for all the fitness scores. The genetic algorithm, by probability, tends to choose the stronger individuals, and the score of this individuals depends on the value we set for each of the $\alpha$ values. This means that the genetic algorithm will reward differently, different transformations of the chromosomes that affect to different rules. 

The fact that there exists this many rules, and the variables for the main structure of the chromosome can vary, implies that sometimes, we will not have a perfect solution that takes all of this rules into account. For example, if there is a person that have 3 weeks of holidays in a month that have 4 weeks, we will not have a perfect score for the rule 3 or 5. This is why it is important to choose all of the values of $\alpha$ in order to satisfy our needs. 

On the other hand, we need to make sure that each of the sub-scores comprehend the same range of values. Otherwise, the model will give a huge importance to some sub-scores that have big values, and will avoid those rules with a smaller value, and this could end up falling into a local maximum. This range will be bounded from -1 to 1 for all of the rules. 

### Selection 

For the selection I used the Roulette Selection. The idea of this method is summing up all the scores of the individuals, choose a random number in this range, and select the first individual in an ordered by maximum list that overpass this value in the cumulative distribution. 

I decided to preserve the best chromosome of each iterations in order to foment the creation of better chromosomes basing on this best individual. With this method we will not lose the advances of finding a really good chromosome, but we will not lose the stochastic factor that allows the algorithm find other good solutions. 

### Crossover

The population is grouped by pairs and crossed to obtain the new evolved population. Crossovers could be accomplished by using different methods. Furthermore, depending on the problem we are solving, some methods can be more fittable for the specific situation. 

I am going to try two different methods for this project.

- Uniform Crossover: The algorithm iterates over the positions of the chromosome. In each iteration, there will be a probability of crossing a certain gene of one of  chromosomes with the gene in the same possition of the other chromosome.  
- K-Points Crossover: Both chromosomes are divided by K parts, and this K parts are mixed alternately to form the childs. 

### Mutation

After crossing over the population, we are going to mutate the chromosomes. Not all the chromosomes are chosen for the mutation, but we will randomly select the part of the population that will be mutated given a probability. The mutation function will change by probability some of the genes of the chosen group.

There are 3 types of mutations in this project.

- Random mutation: The genes chosen will be randomly changed to any of the other possibilities (People).
- Random mutation v2: Similar to the random mutation, but if some people of the population are not included in the information of the chromosome, will be added to the pool of possible changes, if all of the participants are included in the genes, the pool will count with all of the participants.
- Probabilistic mutation: This function gives more importance to the people that are assigned to less tasks in the individual. 

This functions will be tested and compared in the [Experimentation](#Experimentation) section.

### Callbacks

A callback is a function that can interfear in the process of training. There are two possible callbacks in this project. 
- Early stopping: This function will stop the training process if in a number of iterations previously set, there is not an improvement for the best individual. 
- Checkpointing: This function will keep track of the best individual and it will save it into a file when this new chromosome improve it's fitness score.

$~~~~~~~~~~~$

## Plots and Visualization

For the experimentation I used [matplotlib](https://matplotlib.org/) library to plot the best fitness scores for each configuration over the iterations of the training. 

I also used the library [fullcalendar](https://fullcalendar.io/) for visualizing the best chromosome result of the training. I created a React project with this component. To visualize the calendar I changed some properties and everytime I want to obtain the calendar I run the program on the localhost. 

 $~~~~~~~~~~~$

## Experimentation

#### Fixed Variables

<div align="center">

| **Variable**    | **Value** |
|:---------------:|:---------:|
| **Month**       | July      |
| **Year**        | 2022      |
| **$\alpha_1$**  | 0.35      |
| **$\alpha_2$**  | 0.25      |
| **$\alpha_3$**  | 0.15      |
| **$\alpha_4$**  | 0.2       |
| **$\alpha_5$**  | 0.05      |
| **Early Stop**  | False     |
| **Checkpoint**  | True      |
| **Random Seed** | 15        |

 </div>

 $~~~~~$

The random seed will only be set for the population initialization. This seed will make sure that in all runs, we start from the same population, so the experiments made will only depend on the features we want to test.


<div align="center">

### Free days
| **Name**    | **Free Days**     |
|:-----------:|:-----------------:|
| **Alberto** | 1 July - 7 July   |
| **Zarra**   | 1 July - 7 July   |
| **Hatice**  | 21 July - 26 July |
| **Sergio**  | 11 July - 15 July |

</div>

$~~~~~~~~~~~$

### Crossover Selection

This experiment will determine which crossover method seems to work better for the problem itself. 
I only want to test the crossover effectivity, so I set the **mutation probability of the chromosome to 0** so it does not affect to the results. 
The experiment will take **10 tests** for each of the configuration, a population of **75 chromosomes** and **2000 iterations** per training. 

We have 4 possible configurations.

<div align="center">

| **Name**              | **Crossover**         | **Parameters Value**      |
|:---------------------:|:---------------------:|:-------------------------:|
| Configuration 1       | **Uniform Crossover** | 0.75 (Cross Probability)  |
| Configuration 2       | **Uniform Crossover** | 0.9  (Cross Probability)  |
| Configuration 3       | **K-Points**          | 3 (K)                     |
| Configuration 4       | **K-Points**          | 5 (K)                     |

</div>    
    
 $~~~~~~~~~~~$
    
After training the genetic algorithm with all of the configurations, I obtained the following results:

<div align="center">
    
|  |  |
:-----------:|:------------------------------------------------------------------------------------------------------------------------------------------:
| <img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/bestScores_0_config1_cross_test10.jpg" width=500 align=center> | <img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/bestScores_0_config2_cross_test10.jpg" width=500 align=center> |
| <figcaption>Config 1</figcaption> | <figcaption>Config 2</figcaption> |
| <img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/bestScores_0_config3_cross_test10.jpg" width=500 align=center> | <img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/bestScores_0_config4_cross_test10.jpg" width=500 align=center> |
| <figcaption>Config 3</figcaption> | <figcaption>Config 4</figcaption> |    

</div>

This plots shows the fitness scores obtained on each iteration during the training process of the genetic algorithm for all the tests. The continuous and red line shows the mean of all the runs, this will give us an idea of the average performance for each configuration. 
At first sight, we can see that the model converge easily to a good fitness, in only 250 iterations the model increased the score from 0.18 to 0.85. And the following iterations improve the score lowly till we reach a local maximum. 

<dl>
    <dd>
        <dl>
            <dd>
                <h4>Note</h4>
                <dl>
                    <dd>
                        <p>Since all of the sub-scores are ranged from 0 to 1, and all the $\alpha$ values are normalized, the maximum score we can obtain is 1. Also,                            depending on the combination of tasks, free days, people, and days in the calendar, the maximum score possible for each calendar varies.</p>
                    </dd>
                </dl>
            </dd>
        </dl>
    </dd>
</dl>

 $~~~~~~~~~~~$

In the following table, We can see the values obtained for the execution time, and the average fitness obtained in the cuts 250, 500 and 2000.

<div align="center">

| **Configuration** | **Execution time** | **250 iterations Avg Fit** | **500 iterations Avg Fit** | **2000 iterations Avg Fit** |
|:-----------------:|:------------------:|:--------------------------:|:---------------------------:|:---------------------------:|
| **1**             | 9 min              |  0.8556                    |  0.8996                     |  0.9513                     |
| **2**             | 8 min 45 seg       |  0.8887                    |  0.9126                     |  0.9472                     |
| **3**             | 9 min 14 seg       |  0.8656                    |  0.9054                     |  0.9451                     |
| **4**             | 9 min 26 seg       |  0.8629                    |  0.9061                     |  0.9425                     |

</div>

The difference in the execution time for all of the tests for each configuration is not pretty significant. Eventhough, We can see that Uniform Crossover was faster than KPOINTS in this experiments. Talking about the average scores, It seems that both configurations with Uniform Crossover got better results in almost all of the cuts. Because of this two points, up to now, all the rest of experiments will be setted with *Uniform Crossover*. 

Even though the second configuration converged faster the first iterations, it got worst overall results at the end of the run. This is the reason why, I will set the crossover value to *0.75*.
    
### Mutation Selection

**10 tests**, **100 chromosomes** and **1500 iterations**


<div align="center">

| **Name**              | **Mutation**               | **Mutation Probability** | **Probability of Muting the Gene** |
|:---------------------:|:--------------------------:|:------------------------:|:----------------------------------:|
| Configuration 1       | **Random Mutation  **      | 0.1                      | 0.01                               |
| Configuration 2       | **Random Mutation  **      | 0.1                      | 0.05                               |
| Configuration 3       | **Random Mutation  **      | 0.3                      | 0.01                               |
| Configuration 4       | **Random Mutation  **      | 0.3                      | 0.05                               |
| Configuration 5       | **Random Mutation v2**     | 0.1                      | 0.01                               |
| Configuration 6       | **Random Mutation v2**     | 0.1                      | 0.05                               |
| Configuration 7       | **Random Mutation v2**     | 0.3                      | 0.01                               |
| Configuration 8       | **Random Mutation v2**     | 0.3                      | 0.05                               |
| Configuration 9       | **Probabilistic Mutation** | 0.1                      | 0.01                               |
| Configuration 10      | **Probabilistic Mutation** | 0.1                      | 0.05                               |
| Configuration 11      | **Probabilistic Mutation** | 0.3                      | 0.01                               |
| Configuration 12      | **Probabilistic Mutation** | 0.3                      | 0.05                               |
    
</div>  

 $~~~~~~~~~~~$

<div align="center">

| **Configuration**  | **Execution time** | **250 iterations Avg Fit** | **500 iterations Avg Fit** | **2000 iterations Avg Fit** |
|:------------------:|:------------------:|:--------------------------:|:---------------------------:|:---------------------------:|
| **1**              | 7 min 47 seg       |  0.8396                    |  0.8966                     |  0.9369                     |
| **2**              | 8 min              |  0.8549                    |  0.9035                     |  0.9319                     |
| **3**              | 8 min 27 seg       |  0.8475                    |  0.8684                     |  0.9005                     |
| **4**              | 8 min 31 seg       |  0.8563                    |  0.8692                     |  0.9041                     |
| **5**              | 8 min              |  0.8878                    |  0.9053                     |  0.9386                     |
| **6**              | 8 min 9 seg        |  0.8954                    |  0.9112                     |  0.9336                     |
| **7**              | 8 min 37 seg       |  0.8930                    |  0.9112                     |  0.9240                     |
| **8**              | 8 min 38 seg       |  0.8628                    |  0.8846                     |  0.9362                     |
| **9**              | 9 min 55 seg       |  0.8830                    |  0.9100                     |  0.9233                     |
| **10**             | 10 min 35 seg      |  0.8518                    |  0.8673                     |  0.9101                     |
| **11**             | 10 min 25 seg      |  0.8802                    |  0.8864                     |  0.9241                     |
| **12**             | 12 min 55 seg      |  0.8593                    |  0.8736                     |  0.9049                     |

 </div>

As we can see, any of the configurations could improve the performance of the genetic algorithm without mutation. This could means several things:
- Population is not big enough to have diversity in the mutations. 
- The genetic algorithm could converge slower. 
- The mutations chosen are not effective for this problem.

$~~~~~~~~~~~$

## Results

The final results will be obtained using the same scenario than in the [Experimentation](#Experimentation). We will also choose the best configuration which got the best results in a good time during the experiments:

<div align="center">

| **Parameter**                   | **Value**               | 
|:-------------------------------:|:-----------------------:|
| Type Mutation                   | **Random Mutation v2**  | 
| Type of Crossover               | **Uniform Crossover**   | 
| Uniform Crossover Probability   | **0.75**                |
| Population                      | **75**                  | 
| Iterations                      | **100000**              | 

</div>  

$~~~~~~~~~~~$

This are the results after running the genetic algorithm with the configuration for 100000 generations:

<div align="center">

| **Execution time** | **100000 iterations Avg Fit** |
|:------------------:|:-----------------------------:|
| 38 min 48 seg      |  0.9538                       |

 </div>
 
 $~~~~~~~~~~~$

 <div align="center">
    
<img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/ConfigFinal.png" width=1000 align=center><figcaption>Task calendar result of the final configuration</figcaption> 

</div>

In this picture of the calendar, we can observe visually the results of the genetic algorithm. 
First, we can check if each all the rules we setted for having a good calendar are been respected by our algorithm. 
- **Fitness 1**: People can have holidays in which they will not be able to complete a task.
We can observe that any of the people have to make a task on a free day ([Free days](#Free-days))
- **Fitness 2**: The tasks will be equally distributed in between all participants. 
All the participants have 2 tasks assigned, except Zarra that has 1 because there are no more tasks to assign.
- **Fitness 3**: A person will not have more than one task in a day as long as it is possible.
Nobody has 2 tasks in a day as we can observe.
- **Fitness 4**: The type of tasks of each participant will be as diverse as possible.
Nobody has the same task twice. 
- **Fitness 5**: The time in between the tasks of the participants will be as equally distributed as possible. 
The tasks are equally distributed over time, as we can see in the picture. 

 <div align="center">

| Person  | days in between tasks | 
|:-------:|:---------------------:|
| Davor   | 13                    |
| Emma    | 15                    |
| Seda    | 19                    |
| Oscar   | 15                    |
| Biswu   | 13                    |
| Ceren   | 15                    |
| Andriu  | 15                    |
| Ayden   | 14                    |
| Alberto | 16                    |
| Hatice  | 18                    |
| Sergio  | 15                    |
| Zarra   | Only one task         |

</div>    
    
$~~~~~~~~~~~$
 
As we can see the distribution of the tasks in time is very similar. with 6 days of difference in the extreme cases.  
With this example, we can see that the genetic algorithm is able to build a really trustable calendar based on rules that we can customize, it is a strong tool for creating a good task calendar within one hour. 

 <div align="center">
    
<img src="https://github.com/SerBravoSantos/Sergio-Bravo-Santos/blob/gh-pages/graphs/bestScores_0_configFinalCal2_test1.jpg" width=400 align=center><figcaption>Final configuration best fitness</figcaption> 

</div>

Appart from the results obtained in the total run, we can also observe, that the genetic algorithm converges really fast, and then it starts to enhance the fitness of the best chromosome slower. As we can see, there is a turning point in the first 2500 iterations, where it reaches a fitness score of 0.9523, meanwhile at the end of the generations the best chromosome obtained a score of 0.9538. 
Although this score gap could mean a better distributed calendar, or an enhance in any other feature, we can customize the importance we want to give to each feature in order to fasten how fast the genetic algorithm gets a better score in that fitness in specific. This means we could obtain a really good calendar within only 5 minutes. And if we want to optimize it to the maximum, it will take a bit longer. 

$~~~~~~~~~~~$

## Conclusions

This project was really satisfactory. First, the algorithm is able to optimize the task calendar based on the rules we wanted to optimize, so the goal of the project is achieved. We also get this results in a short execution time, as we said, for the example we could get a good fitness score in 2 minutes, and we could obtain an even better result in around 40 minutes. 
The project showed me how to use a genetic algorithm for an unsupervised learning problem, and every step I needed in order to satisfy all the needs:
1. Thinking in the definition of the problem
2. Thinking in the constraints of the problem
3. Define the problem:
    1. Chromosome
    2. Calendar, tasks, people structures.
    3. Fitness Score
4. Programming all the functions neccessary for the algorithm, obtain the genes of the chromosome... 
5. Testing the algorithm with different parameters (Optimization of the algorithm)
I also used different libraries for:
    - Retreiving the calendar. (calendar)
    - Visualizing the calendar. (fullcalendar)
    - Plotting the results. (matplotlib)
    - ML libraries: Numpy (working with vectors)    

<!-- (Maybe adding the weakness of the algorithm, a more technical analysis (with avg exec time and space in memmory of the algorithm)) -->

$~~~~~~~~~~~$

## Future Ideas

The project has been useful and I got the objectives I wanted to achieve. Nevertheless, there are still ways to enhance its performance and utility. 
- Different criterias or subscores for the evaluation function, like adding weighted tasks depending on how much effort does it takes to complete a certain task. This criteria would replace number of tasks assigned per person, instead, we would add the total effort made by each person.
- Change the calendar functions to manage different periods of time like a week, two months, a year...
- Add more mutation functions. An example could be a mutation that permute some of the genes (This could help with the time distribution in between tasks)
- The problem could also be fittable for other unsupervised learning models. 

$~~~~~~~~~~~$

## Usage Guide

To generate a calendar you can follow the next steps:
1. Change config.py file. 
    1. YEAR: Year of the calendar
    2. MONTH: Month of the calendar
    3. PEOPLE: add the people you want to participate in the task calendar and add this people in the getter functions in calendarFunctionS.py
    4. TASKS: create the tasks you want to set for the calendar and add this tasks in the getter functions in calendarFunctionS.py
    5. COLOR: Assign the color for each tasks (This step works for getting the calendar with fullCalendar api)
    6. DAYSOFF: Add the free days where the people will not be able to do tasks
    7. Alphas: Change the alpha values to regulate each of the subfitness values. To check the sub-fitness scores read the following section [Evaluation](#Evaluation)
    8. configs: Create the desired configuration. You will have to change the main file to modify the variable the second parameter when it the function testConfiguration is used. 
2. In the main file you will have to modify:
    1. peopleChosen: Choose the people you want to add in the calendar
    2. load: if you want to load a saved best population from the last run
    3. ntest: number of tests for each configuration you set
    4. tests Flags: If you want to reproduce the experiments set this tests flags to true

If you want to obtain the calendar using fullCalendar, you have to copy the output from textfiles/calendars/calendar_configX.txt inside the events brackets (replace the last calendar if it exists) in the file calendar/client/src/Components/Calendar.jsx
Once done, open the command prompt in calendar/client folder, and run the command npm start (you need to have nodejs installed)
