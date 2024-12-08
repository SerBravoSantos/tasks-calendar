from config import *

""" The functions we need to interact with the calendar are found here
"""

def getDayOfTheWeek(day):
    """ Returns a string of the day of the week passed
    
        Args:
            day (int): Number that represents the day in the enumerate.
        Returns:
            string of the day asked.
    """ 
    if day == MONDAY:
        return "MONDAY"
    elif day == TUESDAY:
        return "TUESDAY"
    elif day == WEDNESDAY:
        return "WEDNESDAY"    
    elif day == THURSDAY:
        return "THURSDAY"
    elif day == FRIDAY:
        return "FRIDAY"
    elif day == SATURDAY:
        return "SATURDAY"
    elif day == SUNDAY:
        return "SUNDAY"
    else:
        return None

def getTask(task):
    """ Returns a string of the task asked.
    
        Args:
            task (int): Number that represents the task in the enumerate.
        Returns:
            string of the task asked.
    """ 
    if task == CBB:
        return "CBB"
    elif task == CSB:
        return "CSB"
    elif task == CK:
        return "CK"    
    elif task == VS:
        return "VS"
    elif task == TOB:
        return "TOB"
    elif task == TIB:
        return "TIB"
    elif task == CTB:
        return "CTB"
    else:
        return "Not Name Assigned"

def getWeek(week):
    """ Returns a string of the week of the month passed
    
        Args:
            week (int): Number that represents the week in the enumerate.
        Returns:
            string of the week asked.
    """ 
    if week == WEEK1:
        return "WEEK 1"
    elif week == WEEK2:
        return "WEEK 2"
    elif week == WEEK3:
        return "WEEK 3"    
    elif week == WEEK4:
        return "WEEK 4"
    elif week == WEEK5:
        return "WEEK 5"
    elif week == WEEK6:
        return "WEEK 6"
    else:
        return None

def getPerson(person):
    """ Returns a string of the person asked.
    
        Args:
            person (int): Number that represents the person in the enumerate.
        Returns:
            string of the person asked.
    """
    if person == ALBERTO:
        return "ALBERTO"
    elif person == OSCAR:
        return "OSCAR"
    elif person == ANDRIU:
        return "ANDRIU"    
    elif person == ZARRA:
        return "ZARRA"
    elif person == AYDEN:
        return "AYDEN"
    elif person == BISWU:
        return "BISWU"
    elif person == CEREN:
        return "CEREN"
    elif person == HATICE:
        return "HATICE"
    elif person == SEDA:
        return "SEDA"
    elif person == EMMA:
        return "EMMA"
    elif person == ALAN:
        return "ALAN"
    elif person == DAVOR:
        return "DAVOR"
    elif person == SERGIO:
        return "SERGIO"
    else:
        return None

def printChromosome(calendarPath, chromosome, calendarStarts, currentCalendar, tasksLenght, tasksGeneral, year, month):
    """ Writes in a file the structure of the calendar where all the people are already assigned by the chromosome passed.
    
        Args:
            calendarPath (str): path where we will write the calendar.
            chromosome (Chromosome): it maps the assignation of the people to the fixed tasks.
            calendarStarts (int): index of the first day of the first week in the calendar.
            currentCalendar (list[list[int]]): calendar we want to write. 
            tasksLenght (int): number of tasks.
            tasksGeneral (dict[str[list[int]]]): dictionary of the fixed tasks by day in a week.
            year (int): Year of the calendar.
            month (int): Month of the calendar. 
    """
    calendarPrint = {}
    for i, gene in enumerate(chromosome):
        i += calendarStarts
        index = i%tasksLenght
        week = int(i/tasksLenght)
        
        dayWeek, task = getDayAndTask(tasksGeneral, index)
        if not week in calendarPrint.keys():
            calendarPrint[week] = {}
        if not dayWeek in calendarPrint[week].keys():
            calendarPrint[week][dayWeek] = []
        calendarPrint[week][dayWeek].append((gene, task))
    strCalendar = ""
    yearStr = str(year)
    monthStr = str(month)
    if len(monthStr) == 1:
        monthStr = "0" + monthStr
    for week, _ in enumerate(currentCalendar):
        for i, day in enumerate(currentCalendar[week]): 
            dayStr = str(day)
            if len(dayStr) == 1:
                dayStr = "0" + dayStr
            if i in calendarPrint[week].keys():
                for _, dupla in enumerate(calendarPrint[week][i]):
                    task = getTask(dupla[1])
                    person = getPerson(dupla[0])
                    strCalendar += "{ title: '" + task + ": " + person + "', date: '" + yearStr \
                                    + "-" + monthStr + "-" + dayStr + "', color: '" + COLOR[dupla[1]] + "' },\n"
    with open(calendarPath, "w+") as f:
        f.write(strCalendar)

def getDayOfTheMonth(chromosome, i):
    """Geths the day of the week and the week of the calendar evaluated having an index passed by argument.

        Args:
            chromosome (Chromosome): chromosome to evaluate
            i (int): index

        Returns:
            week (int): week 
            day (int): day 
    """
    i = chromosome.dayStart + i
    day = i%chromosome.nTasks - 1
    week = int(i/chromosome.nTasks) 
    return week, day

def getDayWeekAddition(currentCalendar):   
    """Some calendars do not start on Monday, this days in the array that do not belong to the month are represented by zero. This function gets the addition for getting the first day.

        Args:
            currentCalendar (list[list[int]]): calendar we want to evaluate
        Returns:
            i (int): addition 
    """
    for i, day in enumerate(currentCalendar[0]):
        if not day == 0:
            return i

def getAddition(tasksGeneral, currentCalendar):
    """As we can start on different days of the week, we need to get the offset of the tasks list we passed to know were we are pointing at. 
        This function calculates the offset of the tasksGeneral.  
        
        Args:
            tasksGeneral (dict[int, list[int]]): Dictionary of the tasks assigned to each day of the week
            currentCalendar (list[list[int]]): calendar we want to evaluate
        
        Returns:
            i (int): addition 
    """
    day = getDayWeekAddition(currentCalendar)
    count = 0
    for dayWeek, tasks in tasksGeneral:
        if day == dayWeek:
            return count
        for _ in tasks:
            count += 1
    return count


def evaluateFreeDays(chromosome, index, person, nGenes):
    """returns a score that evaluates whether the person is assigned to fixed tasks that coincide with a day off for the same person in the schedule. 
        
        Args:
            chromosome (Chromosome): chromosome to evaluate
            index (index of the gene evaluated): _description_
            person (int): number that corresponds to the person evaluated
            nGenes (nGenes): size of the chromosome info

        Returns:
            float: possitive score if the day does not correspond to any day off and negative in the opposite way 
    """
    if DAYSOFF[person]:
        if isTaskOnFreeDay(chromosome, index, person): # If the person not free
            return -1/nGenes
    return 1/nGenes

# If the person assigned to the task is free that day will return true, false if not
def isTaskOnFreeDay(chromosome, index, person):
    """returns whether the day evaluated falls in the range of days of the days off
        
        Args:
            chromosome (Chromosome): chromosome to evaluate
            index (int): index of the gene evaluated
            nGenes (int): size of the chromosome info

        Returns:
        Bool: True if the day does not correspond to any day off and False in the opposite way 
    """
    week, day = getDayOfTheMonth(chromosome, index)
    if DAYSOFF[person]:
        for daysOff in DAYSOFF[person]:
            if daysOff[0][0] == daysOff[1][0] == week:
                if day >= daysOff[0][1] and day <= daysOff[1][1]:
                    return True
            else: 
                if week > daysOff[0][0] and week < daysOff[1][0]:
                    return True
                elif (week == daysOff[0][0] and day >= daysOff[0][1]) or  (week == daysOff[1][0] and day <= daysOff[1][1]):
                    return True
    return False

def getTaskByIndex(chromosome, tasksGeneral, index):
    """Returns the task based on the index of the chromosome
        
        Args:
            chromosome (Chromosome): chromosome to evaluate
            tasksGeneral (dict[int, list[int]]): Dictionary of the tasks assigned to each day of the week
            index (int): index of the gene evaluated

        Returns:
            int: task
    """
    index += getAddition(tasksGeneral.items(), chromosome.calendar)
    i = index%chromosome.nTasks
    
    for _, tasks in tasksGeneral.items():
        for task in tasks:
            if i == 0:
                return task
            i -= 1

def getDayAndTask(tasksGeneral, index):
    """Returns day of the week and the task based on the index. (In this function the index is calculated before)
        
        Args:
            chromosome (Chromosome): chromosome to evaluate
            tasksGeneral (dict[int, list[int]]): Dictionary of the tasks assigned to each day of the week
            index (int): index of the gene evaluated

        Returns:
            int: task
    """
    for dayWeek, tasks in tasksGeneral.items():
        for task in tasks:
            if index == 0:
                return dayWeek, task
            index -= 1