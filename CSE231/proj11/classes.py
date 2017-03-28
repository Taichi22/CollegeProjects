# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 18:43:11 2016

@author: Brian
"""

class Grade(object):
    def __init__(self, assname = "", grade = 0, weight = 0.0):
        """Initializing grade method."""
        self.assignmentName = assname
        if 0 < grade < 100:
            self.grade = grade
        self.weight = weight
    def __str__(self):
        """String representation of the assignment name, grade, and weighting."""
        ret = "Assignment name:" + self.assignmentName + " \nGrade: " + str(self.grade) + " \nWeighting:" + str(self.weight)
        return ret
    def _repr__(self):
        """Convert grade into string for shell usage."""
        return self.__str__()
        
class Student(object):
    def __init__(self, stuid = 0, fname = "", lname = "", gradelist = None):
        self.stuid = stuid
        self.fname = fname
        self.lname = lname
        self.gradelist = gradelist
    def add_grade(self, grade):
        if self.gradelist:
            self.gradelist.append(grade)
        else:
            self.gradelist = []
            self.gradelist.append(grade)
        return True
    def calculate_grade(self):
        finalgr = 0
        for ind in range(len(self.gradelist)):
            finalgr += int(self.gradelist[ind].grade) * float(self.gradelist[ind].weight)
        return finalgr
    def __str__(self):
        """String representation of student object"""
        ret = "{},{}".format(self.lname, self.fname)
        if self.gradelist:
            for i in range(len(self.gradelist)):
                ret+= '\n{}     :   {}%   {:03.2f}'.format(self.gradelist[i].assignmentName, self.gradelist[i].grade, float(self.gradelist[i].weight))
            ret += "\nFinal Grade:   {}%".format(int(self.calculate_grade()))
        else:
            ret += "\nNo Grades"
        return ret
        
    def __repr__(self):
        """String representation for shell usage."""
        return self.__str__()
    def __gt__(self, target):
        """Returns true if the student's grade is greater than a target student's grade."""
        x1 = self.calculate_grade()
        x2 = target.calculate_grade()
        if x1 > x2:
            return True
        elif x2 >= x1:
            return False
        else:
            return False
    def __lt__(self, target):
        """Returns true if a studetn's grade is less than a target student's grade"""
        x1 = self.calculate_grade()
        x2 = target.calculate_grade()
        if x1 < x2:
            return True
        else:
            return False
    def __eq__(self, target):
        """Returns true if a student's grade is within 10**-3 of another student's grade."""
        x1 = self.calculate_grade()
        x1 = abs(x1)
        x2 = target.calculate_grade()
        x2 = abs(x2)
        if ((x1 - x2) < 10**-3) or ((x2 - x1) < 10**-3):
            return True
        else:
            return False