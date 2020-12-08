from flask import Flask, request, render_template, Response
from camera import Camera

app = Flask(__name__)
pi_camera = Camera()


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    while True:
        frame = pi_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/camera')
def camera():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/toggle_sweep', methods=['POST'])
def toggle_sweep():
    pi_camera.should_sweep = not pi_camera.should_sweep
    return 'OK', 202


@app.route('/rotate_servo1', methods=['POST'])
def rotate_servo1():
    pi_camera.should_sweep = False
    rotation = int(request.form['rotation'])
    pi_camera.rotate_servo1(rotation)
    return 'OK', 202


@app.route('/rotate_servo2', methods=['POST'])
def rotate_servo2():
    pi_camera.should_sweep = False
    rotation = int(request.form['rotation'])
    pi_camera.rotate_servo2(rotation)
    return 'OK', 202
