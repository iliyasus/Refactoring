# gradebook.py - журнал оценок студентов (учебный модуль, занятие 19).
# В коде намеренно есть проблемы для линтера (Pylint/Flake8) и форматтера (Black):
# неиспользуемые импорты и переменные, нарушения PEP8, плохие имена,
# потенциальные баги. Исправлять ничего не нужно: запустите инструменты
# и сохраните список предупреждений.
import os, sys
import json
import random

students = {}
PASS_SCORE=60


def addStudent(name,grades=[],group = 'A1'):
    id = len(students)+1
    students[id] = {'name':name,"grades":grades,'group':group}
    return id


def average(list):
    total=0
    for x in list:
        total+=x
    if len(list)==0:
        return 0
    return total/len(list)


def getBest(group):
    best = None
    bestAvg = -1
    for id in students:
        s = students[id]
        if s['group'] == group:
            a = average(s['grades'])
            if a > bestAvg:
                bestAvg = a
                best = s['name']
    return best


def isPassed(id):
    s = students[id]
    if average(s['grades']) >= PASS_SCORE: return True
    else: return False


def addGrade(id,grade):
    if grade < 0 or grade > 100:
        print( "Wrong grade" )
        return False
    students[id]['grades'].append(grade)
    return True


def removeStudent(id):
    try:
        del students[id]
    except:
        print('No such student')


def report(group):
    result = ""
    count = 0
    unused = 10
    for id in students:
        if students[id]['group'] == group:
            count = count + 1
            status = "passed" if isPassed(id) else "failed"
            result = result + str(count) + ". " + students[id]['name'] + " - " + str(round(average(students[id]['grades']),1)) + " (" + status + ")\n"
    if result == None:
        return ""
    return result


def saveToFile(path):
    f = open(path,'w')
    json.dump(students,f)
    f.close()


def loadFromFile(path):
    global students
    f = open(path)
    students = json.load(f)
    f.close()


def randomGrades(n):
    return [random.randint(0,100) for i in range(n)]


def stats(group, minScore, maxScore, onlyPassed, withNames, sortBy):
    count = 0
    for id in students:
        s = students[id]
        if s['group'] == group:
            a = average(s['grades'])
            if a >= minScore and a <= maxScore:
                count += 1
    return f"Total students"


if __name__ == '__main__':
    first = addStudent('Aigerim', [90, 75, 80])
    second = addStudent('Daniyar', [50, 40])
    addGrade(second, 65)
    print(report('A1'))
    print(getBest('A1'))
