#this file contains methods to create timeline images from an array of tuples with (date, temperature)
from matplotlib import pyplot as plt
from multiprocessing import Process
import os

outbox = "/app/visuals"
#returns an in-memory photo to be displayed from an array of tuples.
def createHistogram(times):
    #data 
    buf = io.BytesIO()
    plt.figure(figsize=[10,8])
    plt.title("user temperature")
    plt.xlabel('Date',fontsize=15)
    ply.ylabel('Temperature',fontsize=15)
    plt.plot(times[0],times[1])
    #save the created plot
    plt.savefig(buf,bbox_inches='tight',format='jpg')
    buf.seek(0)
    return buf


