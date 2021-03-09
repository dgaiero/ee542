from flask import Flask,flash, request, redirect, url_for, send_from_directory,Response,render_template,g
from werkzeug.utils import secure_filename
import mysql.connector
import base64
import threading
import subprocess
import socket
import os
import cv2
from imageFaceDetection import frame_to_faceprint
#not sure if this is what we need...
from camera import VideoCamera

UPLOAD_DIR = '/app/images'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

#tests to see if the filename is valid or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('index.html',version=cv2.__version__)

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/profiles")
def allProfiles():
    return """
    <h1>This is where all of the profiles will be viewed.</h1>
    
    """

#working image upload
@app.route("/login/",methods=['GET','POST'])
def login_preimage():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file added')
            return redirect(request.url)
        fFile = request.files['file']
        if fFile.filename == '' or not allowed_file(fFile.filename):
            flash('invalid file')
            return redirect(request.url)
        else:
            filename = secure_filename(fFile.filename)
            fFile.save(os.path.join(app.config['UPLOAD_DIR'],filename))
            return redirect(url_for('login_postimage',filename=filename))

    return """
    <h1> This is your login screen. You should be able to login here. </h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file capture>
        <input type=submit value=Login>
    </form>
    """

#this is where the user should be able to see their timeline if the image is already processed. 
#This is currently working NEED TO ASK JULIAN HOW TO GET FINGERPRINT FROM IMAGE - done
@app.route("/login/<filename>",methods = ['GET'])
def login_postimage(filename):
    error=""

    #first get fingerprint from image filename
    img = cv2.imread(app.config['UPLOAD_DIR'] +"/"+ filename)
    faceprint_data = frame_to_faceprint(img)
    jpg_face_login_text=""
    if faceprint_data == 0:
        jpg_face_login_text = ""
        error+="no face detected/incorrect number of faces in image"
    else:
        face_print,face_image=faceprint_data

        ret, jpeg_face_login = cv2.imencode('.jpg',face_image)
    
        jpg_face_login_text = base64.b64encode(jpeg_face_login)

        try:
            cnx = mysql.connector.connect(
                user='ee542'
                ,password='23doorkingdomsun56useland26chancegold60multiplybrownplace0'
                ,host='192.168.15.2'
                ,database='frfts')
            query = ("SELECT * from ")

        except mysql.connector.Error as err:
            error += str(err)






    #then get the entry in the mysql table
    #then we need to call something to create the image timeline
    #then we need to display the image timeline
    return render_template(("login.html"),photo=jpg_face_login_text,error=error)

if __name__ == "__main__":
    
    app.run(debug=False, host='0.0.0.0') # start the flask frontend
