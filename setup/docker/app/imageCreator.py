#this file contains methods to create timeline images from an array of tuples with (date, temperature)
from matplotlib import pyplot as plt
from multiprocessing import Process
import os
import io

outbox = "/app/visuals"
#returns an in-memory photo to be displayed from an array of tuples.
def createHistogram(times,temps):
    #data 
    buf = io.BytesIO()
    plt.figure(figsize=[10,8])
    plt.title("user temperature")
    plt.xlabel('Date',fontsize=15)
    plt.ylabel('Temperature',fontsize=15)
    plt.plot(times,temps)
    #save the created plot
    plt.savefig(buf,bbox_inches='tight',format='png')
    buf.seek(0)
    return buf


