from flask import Flask
import threading
import subprocess
from listenerBackend import listener
app = Flask(__name__)

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

  </div>
  """
@app.route("/profiles")
def allProfiles():
    return """
    <h1>This is where all of the profiles will be viewed.</h1>
    
    """
@app.route("/login")
def login():
    return """
    <h1> This is your login screen. You should be able to login here. </h1>
    """

def socketSender():
    #just sends information on a python socket

if __name__ == "__main__":
    listen_thread = threading.Thread(target = listener)
    listen_thread.start() # start the listening backend. Could do a fork, but either one seems to work.
    if(test):
        #create a dummy process to test socket communication

    
    app.run(debug=False, host='0.0.0.0') # start the flask frontend
