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
    fig.savefig(variable+'.png')
    

    

    
    
if __name__ == '__main__':
#    plt.style.use('ggplot')
#    pd.set_option('display.width', 1000)
    colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired   
    colors = [colormap(i) for i in np.linspace(0, 1,20)]

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