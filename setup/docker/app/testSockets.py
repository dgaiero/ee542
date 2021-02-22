import time
import socket
from masterobject import MasterObject
if __name__ == "__main__":
    sender = MasterObject()#sends an empty master object
    my_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while(1):
        time.sleep(10)#sleep for 10 seconds
        my_sock.sendall(sender)#now send this over the socket

