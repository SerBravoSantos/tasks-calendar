YEAR = 2022     # YEAR
MONTH = 7       # JUNE
   
# WEEK DAYS
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(0, 7)

# WEEKS
WEEK1, WEEK2, WEEK3, WEEK4, WEEK5, WEEK6 = range(0, 6)

# PEOPLE
ALBERTO, OSCAR, ANDRIU, ZARRA, AYDEN, BISWU, CEREN, HATICE, SEDA, EMMA, ALAN, DAVOR, SERGIO = range(0, 13)

# TASKS
CBB, CSB, CK, VS, TOB, TIB, CTB = range(0, 7)

# CBB = 0     # CLEAN BIG BATHROOM
# CSB = 1     # CLEAN SMALL BATHROOM
# CK = 2      # CLEAN KITCHEN
# VS = 3      # VACUM STAIRS
# TOB = 4     # TAKE OUT BINS
# TIB = 5     # TAKE IN BINS
# CTB = 6     # CHECK THE BINS

COLOR = {
    CBB: 'light-yellow',
    CSB: 'red',
    CK: 'orange',
    VS: 'blue',
    TOB: 'green',
    TIB: 'cyan',
    CTB: 'purple'
}

# If you want to add free days this is an example
#       OSCAR: [((WEEK1, SATURDAY), (WEEK2, MONDAY)), ((WEEK3, TUESDAY), (WEEK4, MONDAY))]
DAYSOFF = {  ALBERTO: [((WEEK1, FRIDAY), (WEEK2, THURSDAY))] 
            ,OSCAR: []
            ,ANDRIU: []
            ,ZARRA: [((WEEK1, FRIDAY), (WEEK2, THURSDAY))]       
            ,AYDEN: []         
            ,BISWU: []
            ,CEREN: []         
            ,HATICE: [((WEEK4, THURSDAY), (WEEK5, TUESDAY))]                                             
            ,SEDA: []                                            
            ,EMMA: []        
            ,ALAN: []       
            ,DAVOR: []                                            
            ,SERGIO: [((WEEK3, MONDAY), (WEEK3, FRIDAY))]
        }

# Types of mutation
RANDOM_MUTATION = 0
RANDOM_MUTATION_PEOPLE_NOT_IN = 1
RANDOM_MUTATION_PEOPLE_PROP = 2

# Types of crossovers
KPOINT = 0
UNIFORMCROSSOVER = 1

# Selection
ROULETTE = 0

# Evaluation subfitness
alpha1 = 0.35
alpha2 = 0.25
alpha3 = 0.15
alpha4 = 0.20
alpha5 = 0.05

# CONFIGURATION FOR THE HYPER-PARAMETER SELECTION
configsCrossoverTest = {
    # First 6 configs will test the type of Mutation and type of cross overs
    "config1_cross": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": UNIFORMCROSSOVER,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0,
        "kpoints": 3, 
        "uniformCrossValue": 0.75, 
        "population": 75, 
        "iterations": 2000,
        "cuts": [250, 500, 2000]
    },
    "config2_cross": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": UNIFORMCROSSOVER,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0,
        "kpoints": 5, 
        "uniformCrossValue": 0.9, 
        "population": 75, 
        "iterations": 2000,
        "cuts": [250, 500, 2000]
    },
    "config3_cross": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": KPOINT,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 75, 
        "iterations": 2000,
        "cuts": [250, 500, 2000]
    },
    "config4_cross": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": KPOINT,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0,
        "kpoints": 5, 
        "uniformCrossValue": 0.5, 
        "population": 75, 
        "iterations": 2000,
        "cuts": [250, 500, 2000]
    },
}

mutations = [RANDOM_MUTATION, RANDOM_MUTATION_PEOPLE_NOT_IN, RANDOM_MUTATION_PEOPLE_PROP]
mutationProbs = [0.1, 0.3]
mutationGeneProbs = [0.01, 0.05]
configMutationTest = { "config{}_mut".format(1+(i*len(mutationGeneProbs)*len(mutationProbs))+(j*len(mutationGeneProbs))+k) 
                        : {
                            "typeMutation": mutations[i],
                            "typeCrossover": UNIFORMCROSSOVER, 
                            "mutationProb": mutationProbs[j],
                            "mutationGeneProb": mutationGeneProbs[k], 
                            "kpoints": 0, 
                            "uniformCrossValue": 0.75,  
                            "population": 75, 
                            "iterations": 2000,
                            "cuts": [250, 500, 2000]
                        } for i in range(len(mutations)) for j in range(len(mutationProbs)) for k in range(len(mutationGeneProbs)) }


mutationProbs = [0, 0.1]
populations = [75, 125]

configMutationTest2 = { "config{}_mut2".format(1+(i*len(populations))+j) 
                        : {
                            "typeMutation": RANDOM_MUTATION_PEOPLE_NOT_IN,
                            "typeCrossover": UNIFORMCROSSOVER, 
                            "mutationProb": mutationProbs[i],
                            "mutationGeneProb": 0.01, 
                            "kpoints": 0, 
                            "uniformCrossValue": 0.75,  
                            "population": populations[j], 
                            "iterations": 10000,
                            "cuts": [250, 500, 2000, 5000, 10000]
                        } for i in range(len(mutationProbs)) for j in range(len(populations)) }

configFinal = { 'name': "configFinalCal2",
                'parameters' :  {
                                    "typeMutation": RANDOM_MUTATION_PEOPLE_NOT_IN,
                                    "typeCrossover": UNIFORMCROSSOVER,
                                    "mutationGeneProb": 0.01, 
                                    "mutationProb": 0,
                                    "kpoints": 5, 
                                    "uniformCrossValue": 0.75, 
                                    "population": 75, 
                                    "iterations": 100000,
                                    "cuts": [250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
                    },
                }
