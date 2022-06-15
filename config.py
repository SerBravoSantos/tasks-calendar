from sre_constants import RANGE


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
DAYSOFF = {  ALBERTO: [] 
            ,OSCAR: []
            ,ANDRIU: []
            ,ZARRA: []       
            ,AYDEN: []         
            ,BISWU: []
            ,CEREN: []         
            ,HATICE: []                                             
            ,SEDA: []                                            
            ,EMMA: []        
            ,ALAN: []       
            ,DAVOR: []                                            
            ,SERGIO: []
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

# CONFIGURATION FOR THE HYPER-PARAMETER SELECTION

configs = {
    # First 6 configs will test the type of Mutation and type of cross overs
    "config1": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": UNIFORMCROSSOVER,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0.5,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 200, 
        "iterations": 800
    },
    "config2": {
        "typeMutation": RANDOM_MUTATION_PEOPLE_NOT_IN,
        "typeCrossover": UNIFORMCROSSOVER,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0.5,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 200, 
        "iterations": 800
    },
    # "config3": {
    #     "typeMutation": RANDOM_MUTATION_PEOPLE_PROP,
    #     "typeCrossover": UNIFORMCROSSOVER,
    #     "mutationGeneProb": 0.05, 
    #     "mutationProb": 0.5,
    #     "kpoints": 3, 
    #     "uniformCrossValue": 0.5, 
    #     "population": 200, 
    #     "iterations": 1000
    # },
    "config3": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": KPOINT,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0.5,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 200, 
        "iterations": 800
    },
    "config4": {
        "typeMutation": RANDOM_MUTATION_PEOPLE_NOT_IN,
        "typeCrossover": KPOINT,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0.5,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 300, 
        "iterations": 2000
    },
    "config6": {
        "typeMutation": RANDOM_MUTATION,
        "typeCrossover": KPOINT,
        "mutationGeneProb": 0.05, 
        "mutationProb": 0.5,
        "kpoints": 3, 
        "uniformCrossValue": 0.5, 
        "population": 500, 
        "iterations": 20000
    },
    #     "config7": {
    #     "typeMutation": RANDOM_MUTATION_PEOPLE_PROP,
    #     "typeCrossover": UNIFORMCROSSOVER,
    #     "mutationGeneProb": 0.15, 
    #     "mutationProb": 0.75,
    #     "kpoints": 3, 
    #     "uniformCrossValue": 0.75, 
    #     "population": 200, 
    #     "iterations": 10
    # }
}
