from flask import Flask,flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import threading
import subprocess
import socket
import os
from listenerBackend import listener
from imageFaceDetection import frame_to_faceprint
#not sure if this is what we need...
from camera import VideoCamera

UPLOAD_DIR = '/app/images'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR


#tests to see if the filename is valid or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
  return """
  <h1>FRFTS</h1>
  <p>Facial Recognition Forehead Temperature Sensor</p>
  <div> 
  <h2>Important Links:</h2>
    <ul>
    <li><a href="/profiles">Profiles Page</a></li>
    <li><a href="/login">Login Page</a> (which will end up being the only page viewable)</li>
    </ul>
    <h1>Video Stream</h1>
    <img id="bg" src="{{ url_for('video_feed') }}">

  </div>
  """

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame'

@app.route("/profiles")
def allProfiles():
    return """
    <h1>This is where all of the profiles will be viewed.</h1>
    
    """

#working image upload
@app.route("/login",methods=['GET','POST'])
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
        <input type=submit value=Upload>
    </form>
    """

#this is where the user should be able to see their timeline if the image is already processed. 
#This is currently working NEED TO ASK JULIAN HOW TO GET FINGERPRINT FROM IMAGE - done
@app.route("/login/<filename>")
def login_postimage(filename):
     
    return send_from_directory(app.config['UPLOAD_DIR'],filename)

if __name__ == "__main__":
    listen_thread = threading.Thread(target = listener)
    listen_thread.start() # start the listening backend. Could do a fork, but either one seems to work.

    
    app.run(debug=False, host='0.0.0.0') # start the flask frontend
