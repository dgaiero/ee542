#this file contains methods to create timeline images from an array of tuples with (date, temperature)
from matplotlib import pyplot as plt
from multiprocessing import Process
import os

outbox = "/app/visuals"

def createHistogram(data, endLocation,identifier):
    #data 
    plt.figure(figsize=[10,8])
    plt.title(identifier.toString())
    plt.xlabel('Date',fontsize=15)
    ply.ylabel('Temperature',fontsize=15)
    plt.plot(data[0],data[1])
    #save the created plot
    plt.savefig(outbox+"/"+identifier.toString(),bbox_inches='tight')


