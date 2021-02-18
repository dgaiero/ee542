import time
from masterobject import MasterObject
if __name__ == "__main__":
    sender = MasterObject()
    while(1):
        time.sleep(10)#sleep for 10 seconds
        sender.toJson()#now send this over the socket

