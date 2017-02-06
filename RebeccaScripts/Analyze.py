# -*- coding: utf-8 -*-
"""
This is used for analyzing the data in csv files.
largestValue method
    this will get the largest, smallest and average of all values in a given file
"""

def largestValue(fileName):
    Values = open(fileName, "r")
    x = 0
    x1 = 0
    y1 =0 
    y = 360.0
    average = 0
    lines = 0
    next(Values)
    for line in Values:
        line = line.strip();
        coms = line.split(",")
        if float(coms[1]) <= float(y):
            y = coms[1]
            y1 = coms[0]
        if float(coms[1]) >= float(x):
            x = coms[1]
            x1 = coms[0]
        average = average + float(coms[1])
        lines = lines + 1
    print "x " + str(x1) + " " + str(x)
    print "y " + str(y1) + " " + str(y)
    print str(average/lines) + " " + str(lines)
    

if __name__ == '__main__':
    fileName = "Jacob1.csv"
    largestValue("0.14.6899.10806/" + fileName)
    print "\n"
    largestValue("6.1.8230.945/" + fileName)
    print "\n"
    largestValue("7.1.7089.1113/" + fileName)