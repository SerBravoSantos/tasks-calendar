import os
from config import *

dirPath = os.path.dirname(os.path.realpath(__file__))
calendarPath = os.path.join(dirPath, "calendar.txt")

def getDayOfTheMonth(chromosome, i):
    i = chromosome.dayStart + i
    day = i%chromosome.nTasks - 1
    week = int(i/chromosome.nTasks) 
    return week, day

def getDayWeekAddition(currentCalendar):   
    for i, day in enumerate(currentCalendar[0]):
        if not day == 0:
            return i

def getAddition(tasksGeneral, currentCalendar):
    day = getDayWeekAddition(currentCalendar)
    count = 0
    for dayWeek, tasks in tasksGeneral:
        if day == dayWeek:
            return count
        for _ in tasks:
            count += 1
    return count

def getTaskByIndex(chromosome, tasksGeneral, index):
    index += getAddition(tasksGeneral.items(), chromosome.calendar)
    i = index%chromosome.nTasks
    
    for _, tasks in tasksGeneral.items():
        for task in tasks:
            if i == 0:
                return task
            i -= 1

def getDayAndTask(tasksGeneral, index):
    for dayWeek, tasks in tasksGeneral.items():
        for task in tasks:
            if index == 0:
                return dayWeek, task
            index -= 1

def getDayOfTheWeek(day):
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



def printChromosome(chromosome, calendarStarts, currentCalendar, tasksLenght, tasksGeneral, year, month):
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
        monthstr = "0" + monthStr
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
                                    + "-" + monthstr + "-" + dayStr + "', color: '" + COLOR[dupla[1]] + "' },\n"
    with open(calendarPath, "w+") as f:
        f.write(strCalendar)