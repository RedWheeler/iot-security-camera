from flask import Flask, request, render_template, Response
from camera import Camera

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


@app.route('/rotate_servo1', methods=['POST'])
def rotate_servo1():
    rotation = request.form['rotation']
    camera.rotate_servo1(rotation)
    return 'OK', 202


@app.route('/rotate_servo2', methods=['POST'])
def rotate_servo2():
    rotation = request.form['rotation']
    camera.rotate_servo2(rotation)
    return 'OK', 202
