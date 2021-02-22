import socket
import multiprocessing

def listener():
    #this is what will listen over a socket
    host = socket.gethostname()
    port = 51234
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    while(1):
        s.sendall(b'hello')
        #a busy thread
        #wait for some data to come in over a socket
        pass
    return
