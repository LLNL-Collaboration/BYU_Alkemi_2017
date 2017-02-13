"""
simple program to take a csv file and turn it into a graph
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def linePlot(fileName, variable, c):
    """ Create a line graph. """
    data = pd.read_csv(fileName)
    plt.figure()
    ax = data.plot(x='Time',y=variable, label=variable, color=c)
    fig =  ax.get_figure()  
    fig.savefig("6.1.8230.945fc/averageOddyValues/" + str(variable)+'.png')
    

    

    
    
if __name__ == '__main__':
#    plt.style.use('ggplot')
#    pd.set_option('display.width', 1000)
    colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired   
    colors = [colormap(i) for i in np.linspace(0, 1,20)]
              
    folderName = "6.1.8230.945fc/averageOddyValues"
    linePlot(str(folderName) + "/AvgValues0.csv", "0", colors[0])
    linePlot(str(folderName) + "/AvgValues1.csv", "1", colors[1])
    linePlot(str(folderName) + "/AvgValues2.csv", "2", colors[2])
    linePlot(str(folderName) + "/AvgValues3.csv", "3", colors[3])
    linePlot(str(folderName) + "/AvgValues4.csv", "4", colors[4])
    linePlot(str(folderName) + "/AvgValues5.csv", "5", colors[5])
    linePlot(str(folderName) + "/AvgValues6.csv", "6", colors[6])
    linePlot(str(folderName) + "/AvgValues7.csv", "7", colors[7])
    linePlot(str(folderName) + "/AvgValues8.csv", "8", colors[8])
    linePlot(str(folderName) + "/AvgValues9.csv", "9", colors[9])
    linePlot(str(folderName) + "/AvgValues10.csv", "10", colors[10])
    linePlot(str(folderName) + "/AvgValues11.csv", "11", colors[11])
              
    """
    linePlot("Volume1.csv", "Volume", colors[0])
    linePlot("AR1.csv", "AR", colors[1])
    linePlot("CN11.csv", "CN", colors[2])
    linePlot("Dist1.csv", "Dist", colors[3])
    linePlot("Jacob1.csv", "Jacob", colors[4])
    linePlot("LAng1.csv", "LAng", colors[5])
    linePlot("OddyFile1.csv", "Oddy", colors[6])
    linePlot("ScaJac1.csv", "ScaJac", colors[7])
    linePlot("Shape1.csv", "Shape", colors[8])
    linePlot("SandS1.csv", "SandS", colors[9])
    linePlot("Shear1.csv", "Shear", colors[10])
    linePlot("ShanSi1.csv", "ShanSi", colors[11])
    linePlot("Skew1.csv", "Skew", colors[12])
    linePlot("SmAng1.csv", "SmAng", colors[13])
    linePlot("Stretch1.csv", "Stretch", colors[14])
    linePlot("Taper1.csv", "Taper", colors[15])
    linePlot("TotalAngle.csv", "TotalAngle", colors[16])
    """