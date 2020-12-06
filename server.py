from flask import Flask, request, render_template, Response, send_file
from camera import Camera
from subprocess import Popen, PIPE
app = Flask(__name__)

camera = Camera()

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera')
def camera():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rotate', methods=['POST'])
def rotate():
    rotation = request.form['rotation']
    camera.rotate_servo1(rotation)
    return 'OK'

@app.route('/sweep', methods=['POST'])
def sweep():
    return 'OK'
