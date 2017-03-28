# This is a sample proj11-test.py program
# There are two requirements:
#   A) Demonstrate all methods (except __repr__ which can only be demonstrated in the Python shell)
#   B) Include print statements so your output can be read and understood without reading the code

import classes

print("Create a Grade instance: p01, 75, .8")
g1 = classes.Grade("p01",75,.8)    # tests __init__
print("Print the Grade instance")
print(g1)        # tests __str__
# we cannot test __repr__ in a program, only in the Python shell

# Create another grade instance, let's call it g2
# Maybe create more grades
# Create a Student instance, let's call it s1
# Then print s1, include descriptive print statements such as above
# Demonstrate add_grade and calculate_grade
# Create another student instance, let's call it s2
# Demonstrate comparison operators 
g2 = classes.Grade("p02", 90, .6)
s1 = classes.Student(1123, "John", "Doe")
print()
print()
print("Student print test: " + s1.__str__())
s1.add_grade(g1)
s1.add_grade(g2)
print()
print()
print("Grades added: " + s1.__str__())
s2 = classes.Student(1231, "Jane", "Doe")
print()
print()

g3 = classes.Grade("p03", 85, .7)
s2.add_grade(g1)
s2.add_grade(g3)
print("Student 2 print test: " + s2.__str__())
print("\n\n")
print("Testing grade comparisons:")
print("Jane's final grade is: " + str(s2.calculate_grade()))
print("John's final grade is: " + str(s1.calculate_grade()))
print("John Doe's grade greater than Jane's? " + str(s1 > s2))
print("John Doe's grade less than Jane's? " + str(s1 < s2))
print("John Doe's grade equal to Jane's? " + str(s1 == s2))
