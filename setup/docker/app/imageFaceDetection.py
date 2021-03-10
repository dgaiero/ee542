import cv2
import numpy as np

def frame_to_faceprint(frame): # frame is a mat
    haar_face_cascade = cv2.CascadeClassifier('/app/haarcascade_frontalface_default.xml') # initialize haar cascade
    frame_array = np.copy(frame) # make a numpy array copy of the input frame
    faces = haar_face_cascade.detectMultiScale(frame_array[:,:,1], scaleFactor = 1.1, minSize = (4,4), minNeighbors = 6) # create an array of the faces in the frame
    if len(faces) != 1:
       return 0 # exit if more than one face in frame or if no face in frame
    face = faces[0]
    face_net = cv2.dnn.readNetFromCaffe('/app/bvlc_googlenet.prototxt', '/app/bvlc_googlenet.caffemodel') # load dnn
    face_crop = frame_array[face[1]:face[1] + face[3], face[0]:face[0] + face[2], :] # crop frame to just include face
    face_blob = cv2.dnn.blobFromImage(face_crop, 1, (224, 224))
    face_net.setInput(face_blob) # set the dnn's input to the face blob
    face_print = face_net.forward() # retrieve output of dnn (faceprint)
    
    return face_print,face_crop
    

