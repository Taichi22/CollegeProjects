# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:24:58 2016

@author: Brian
"""

import classes
def main():
    x = ""
    lineno = 0
    gradeno = 0
    scoreslist = []
    studentslist = []
    gradelist = []
    while x != "Q":
        try:
            students = open("students.txt")
            grades = open("grades.txt")
            print("Files opened.")
            break
        except FileNotFoundError:
            print("Files not found; try again? \"Q\" will end the program")
            x = input()
    for line in grades:
        if lineno == 0:
            weightlist = line.split()
        if lineno == 1:
            projlist = line.split()
        if lineno > 1:
            scoreslist.append(line.split())
        lineno += 1
    lineno = 0
    #for line in students:
    #print(weightlist, projlist, scoreslist)
    """Parsing through grades"""
    for student in range(len(scoreslist)):
        holdlist = []
        for project in range(len(projlist)-1):
            grade = classes.Grade(projlist[project+1], int(scoreslist[student][project+1]), weightlist[project+1])
            hold = (grade, student) 
            holdlist.append(hold)
        gradelist.append(holdlist)
    """Parsing through students"""
    for line in students:
        student = (line.split())
        studentslist.append(classes.Student(student[0], student[1], student[2]))
    for lists in gradelist:
        for tup in lists:
            for student in studentslist:
                if int(tup[1]+1) == int(student.stuid):
                    student.add_grade(tup[0])
    for student in studentslist:
        print(student)
main()