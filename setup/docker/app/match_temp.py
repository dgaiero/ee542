################################################################################
# MLX90640 Test with Raspberry Pi
################################################################################

import os
import time
from datetime import datetime
from pathlib import Path

import adafruit_mlx90640
import board
import busio
import cv2
import mariadb
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from scipy import ndimage

class thermal_camera:
    therm_width = 32
    therm_height = 24
    mlx_interp_val = 10

    
    def __init__(self, top_cutoff, bottom_cutoff, right_cutoff, left_cutoff, rpi_width, rpi_height, norm):

        load_dotenv()
        self.first_loop = 1
        # Calibrate the thermal camera with the Rpi Camera
        self.top_cutoff = int(top_cutoff)
        self.bottom_cutoff = int(bottom_cutoff) 
        self.right_cutoff = int(right_cutoff)
        self.left_cutoff = int(left_cutoff)
        self.rpi_width = rpi_width 
        self.rpi_height = rpi_height
        self.norm = norm

        # calc the width and height of thermal camera frame
        self.frame_width = self.right_cutoff - self.left_cutoff
        self.frame_height = self.bottom_cutoff - self.top_cutoff

        # Determine Scaled Values
        self.scaled_width = self.rpi_width/self.frame_width
        self.scaled_height = self.rpi_height/self.frame_height

        # Set up the Thermal Camera
        i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
        self.mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
        self.mlx_shape = (self.therm_height,self.therm_width) # Set the shape
        self.mlx_interp_shape = (self.mlx_shape[0]*self.mlx_interp_val, # Interp shape
                self.mlx_shape[1]*self.mlx_interp_val)
        try:
            self.connection = mariadb.connect(user=os.getenv("SQL_USER"),\
                    password=os.getenv("SQL_PASSWORD"),\
                    database=os.getenv("SQL_DATABASE"), host=os.getenv("SQL_HOST"))
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Users( face_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
                    "face_print MEDIUMBLOB, frame MEDIUMBLOB) ") 
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Temps( temp_num INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
                    "userId INT UNSIGNED , time DATETIME, temp INT UNSIGNED,"
                    "FOREIGN KEY (userId) REFERENCES Users (face_id) ON DELETE CASCADE )")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        #   def send_data( self ):

    def get_temp(self, person):
       
        # Get the current temperature data
        therm_frame = np.zeros(self.mlx_shape[0]*self.mlx_shape[1]) # 768 temps
        self.mlx.getFrame(therm_frame) # read mlx90640
        data_array = np.fliplr(np.reshape(therm_frame, self.mlx_shape)) # reshape and flip
        data_array = ndimage.zoom(data_array, self.mlx_interp_val) # interpolate
        
        # Match forehead box coordinates thermal camera coordinates
        self.start_x = int(round(person.forehead[0]/self.scaled_width)) + self.left_cutoff
        self.start_y = int(round(person.forehead[1]/self.scaled_height)) + self.top_cutoff
        self.end_x = int(round(person.forehead[2]/self.scaled_width)) + self.left_cutoff
        self.end_y = int(round(person.forehead[3]/self.scaled_height)) + self.top_cutoff
        
        # Now get just the temps of interest into an array
        forehead_array = np.zeros([(self.end_y-self.start_y), (self.end_x - self.start_x)])
        forehead_array = data_array[self.start_y:self.end_y+1, self.start_x:self.end_x+1]
        temp = np.mean(forehead_array)
        print('Average forehead temp: {0:2.1f}C ({1:2.1f}F)'.\
                format(temp, ((9.0/5.0)*temp+32.0)))
        
        # Format the date
        formatted_date = datetime.now() 
        
#        face_print = np.linalg.norm(face_net.forward()[0])
        # Check norm against norms in table

        # Get the max id value
        Q = ''' SELECT MAX(face_id) FROM Users'''
        self.cursor.execute(Q)
        max_id = self.cursor.fetchall()
        maxxx = max_id[0][0]
        print('Maxxx: ', maxxx)
        norm  = 1
        if( self.first_loop ):
            norm = 1
            self.first_loop = 0
            max_id = 1
        else:
            x = 1
            while x <= maxxx:
                print('X: ',x)
                # Extract and convert the face_print
#                Q = ''' SELECT face_print FROM Users WHERE face_id = %s;'''
#                val = (x,)
#                self.cursor.execute(Q, val)
                
                self.cursor.execute(f"SELECT face_print FROM Users WHERE face_id = {x};")
                
                fp_string = self.cursor.fetchone()
#                print('FP_string: ', fp_string)
#                print('Length: ', len(fp_string))
                fp_array = np.frombuffer(fp_string[0], np.uint8)
#                print('FP_array: ', fp_array)
                fp = cv2.imdecode(fp_array, cv2.IMREAD_GRAYSCALE)
                
                # Compare the two face_prints
                norm = np.linalg.norm(person.face_print - fp)
                same_face_id = x
                print('Same Face Id: ', same_face_id)
                print('Norm: ',norm)
                if norm < self.norm:
                    break
                x = x+1

        if norm > self.norm:
            print('No match')
            
            # Convert the frame image to a string
            img_str = cv2.imencode('.jpg', person.frame)[1].tostring()
            fp_str = cv2.imencode('.jpg', person.face_print)[1].tostring()
#            print('New face_print: ', fp_str)
            
            # Insert the frame into the table
            Q1 = '''INSERT INTO Users (face_print, frame) VALUES (%s, %s)''' 
            val1 = (fp_str, img_str,)
            self.cursor.execute(Q1,val1)

            # Convert the face_print to a string
            # Insert the face_print into the table
#            Q2 = '''INSERT INTO Users (face_print) VALUES (%s)''' 
#            val2 = (fp_str,)
#            self.cursor.execute(Q2,val2)
            
            # Get the face_id corresponding to the new face_print
#            self.cursor.execute(f"SELECT face_id FROM Users "
#                    f"WHERE face_print = {person.face_print};")
#            new_id = self.cursor.fetchall()

            # Insert the time and temp with the new face_id
            Q3 = "INSERT INTO Temps (userId, time, temp) VALUES (%s,%s,%s)"
            val3 = (maxxx, formatted_date, person.temperature)
            self.cursor.execute(Q3,val3)
        
        else:
            print('Found a match')

            # Insert the time and temp with the matching face_id
            Q4 = "INSERT INTO Temps (userId, time, temp) VALUES (%s,%s,%s)"
            val4 = (same_face_id, formatted_date, person.temperature)
            self.cursor.execute(Q4,val4)
        
        self.connection.commit()

    def close_connect(self):
        self.connection.close()
    
    def set_figure(self):
        # setup the figure for plotting
        plt.ion() # enables interactive plotting
        self.fig = plt.figure(figsize=(12,9))
        self.ax = self.fig.add_subplot(111) # add subplot
        self.fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of padding
        self.therm1 = self.ax.imshow(np.zeros(self.mlx_interp_shape), interpolation = 'none',
                cmap = plt.cm.bwr, vmin = 25, vmax = 45) # start plot with zeros
        self.cbar = self.fig.colorbar(self.therm1) # setup colorbar for temps
        self.cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)

        self.fig.canvas.draw()
        self.ax_background = self.fig.canvas.copy_from_bbox(self.ax.bbox) # copy background
        self.fig.show()

        self.frame = np.zeros(self.mlx_shape[0]*self.mlx_shape[1]) # 768 temps

    def plot_update(self):
        self.fig.canvas.restore_region(self.ax_background) # restore background
        self.mlx.getFrame(self.frame) # read mlx90640
        data_array = np.fliplr(np.reshape(self.frame, self.mlx_shape)) # reshape and flip
        data_array = ndimage.zoom(data_array, self.mlx_interp_val) # interpolate
        self.therm1.set_array(data_array) # set data
        self.therm1.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))
        self.cbar.on_mappable_changed(self.therm1) # update colorbar range

        self.ax.draw_artist(self.therm1) # draw new thermal image
        self.fig.canvas.blit(self.ax.bbox) # draw background
        rect = patches.Rectangle((self.start_x,self.start_y), (self.end_x - self.start_x),
                (self.end_y - self.start_y), linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(rect)
        self.fig.canvas.flush_events() # show the new image
        return

class user:
    def __init__(self, face_print, forehead, temperature, frame, time ):
        self.face_print = face_print
        self.forehead = forehead
        self.temperature = temperature
        self.frame = frame
        self.time = time

def frame_to_person(frame_array):
    haar_face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame_array,cv2.COLOR_BGR2GRAY)
    faces = haar_face_cascade.detectMultiScale(gray,1.1,3)
    if len(faces) != 1:
        print("Faces in frame != 1")
        return 0
    face = faces[0]
    for (x,y,w,h) in faces:
        cv2.rectangle(frame_array, (x,y), (x+w,y+h), (0,0,255), 3)
        start_x = x + w//4
        start_y = y + h//8
        end_x = x+3*w//4
        end_y = y+h//4
        forehead = [start_x, start_y, end_x, end_y]
        cv2.rectangle(frame_array, (start_x,start_y), (end_x,end_y), (0,0,255), 2)
        t = time.ctime(time.time())
        cv2.putText(frame_array, t, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        face_net = cv2.dnn.readNetFromCaffe('bvlc_googlenet.prototxt','bvlc_googlenet.caffemodel')
        face_crop = frame_array[face[1]:face[1] + face[3], face[0]:face[0] + face[2], :]
        face_blob = cv2.dnn.blobFromImage(face_crop,1,(224,224))
        face_net.setInput(face_blob)
#        face_print = np.linalg.norm(face_net.forward()[0])
        face_print = face_net.forward()
        person = user(face_print, forehead, 0, frame_array, t)
        return person

if __name__ == "__main__":
    from camera import VideoCamera
    camera = cv2.VideoCapture(0)
    try:
        print('Starting RPi camera')
        start_x = 300 
        start_y = 400
        end_x = 340
        end_y = 425 
        top_cutoff = 0
        bottom_cutoff = 220
        right_cutoff = 275
        left_cutoff = 45
        rpi_width = 1280
        rpi_height = 720
        norm = 0.7
        forehead = [start_x, start_y, end_x, end_y]
        therm_cam = thermal_camera( top_cutoff, bottom_cutoff, right_cutoff,
                left_cutoff, rpi_width, rpi_height, norm)
        
        while(1):
            time.sleep(0.1)
            _, image = camera.read()
            person = frame_to_person(image)
        
            if person == 0:
                print("Error")
            else:
                therm_cam.get_temp(person)
                cv2.putText(person.frame, str(person.temperature), (10,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Image", person.frame)
                cv2.waitKey(10)
    finally:
        print ("releasing camera")
        camera.release()
