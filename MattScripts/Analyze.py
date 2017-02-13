# -*- coding: utf-8 -*-
import time
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
    slope = 0
    previous = 0
    count = 0
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
        temp = float(coms[1]) - float(previous)
        slope += temp
        if float(temp) > 1:
            count +=1
        previous = float(coms[1])
        average = average + float(coms[1])
        lines = lines + 1
    print "x " + str(x1) + " " + str(x)
    print "y " + str(y1) + " " + str(y)
    print "Average value " + str(average/lines) + " " + str(lines)
    print "Average Slope " + str(slope/lines)
    print "High Slopes " + str(count)
    
    
def completeAveraging():
    specifics = open("specifics.csv","w")
    specifics.write("type,file,zone,value\n")
    start = time.time()
    AV = 0
    x = 0
    x1 = 0
    avgval = 0
    avgslo = 0
    BigSlo = 0
    BigVal = 0
    LSlope = 0
    LargestValues = 0
    LargestSlopes = 0

    while AV <= 11:
        sx = 0
	sx1 = 0
	savgval = 0
	savgslo = 0
	sBigSlo = 0
	sBigVal = 0
	sLSlope = 0
	lineNum = 0
        values = open("AvgValues" + str(AV) + ".csv", "r")
        next(values)
        for line in values:
            line = line.strip()
            coms = line.split(",")
	    if float(coms[4])  > 1000000:
	    	LargestValues += 1
		specifics.write("A," + str(AV) + "," + str(lineNum) + "," + str(coms[4]) + "\n")
            sx += float(coms[4])
            sx1 += float(coms[5])
            savgval += float(coms[6])
            savgslo += float(coms[7])
            sBigSlo += float(coms[8])
            sBigVal += float(coms[9])
            sLSlope += float(coms[10])       
	    if float(coms[12]) > 1000000:
	    	LargestSlopes += 1
		specifics.write("B," + str(AV) + "," + str(lineNum) + "," + str(coms[10]) + "\n")

	    lineNum +=1
        AV += 1
	x += float(sx/lineNum)
	x1 += float(sx1/lineNum)
	avgval += float(savgval/lineNum)
	avgslo += float(savgslo/lineNum)
	BigSlo += float(sBigSlo/lineNum)
	BigVal += float(sBigVal/lineNum)
	LSlope += float(sLSlope/lineNum)
	print time.time() - start
        
    print "Highest Value " + str(float(x/11))
    print "Highest Cycle " + str(float(x1/11))
    print "Average Value " + str(float(avgval/11))
    print "Average Slope " + str(float(avgslo/11))
    print "Slope > 1 " + str(float(BigSlo/11))
    print "Value > 100 " + str(float(BigVal/11))
    print "Largest Slope " + str(float(LSlope/11))
    print "Largest Values overall > 1000000 " + str(LargestValues)
    print "Largest Slopes overall > 1000000 " + str(LargestSlopes)
    
    
if __name__ == '__main__':
    fileName = "OddyFile1.csv"
    completeAveraging()
    #print "\n"
    #largestValue("6.1.8230.945fc/" + fileName)
    #print "\n"
    #largestValue("7.1.7089.1113" + "/" + fileName)
