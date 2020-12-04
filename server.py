from flask import Flask, request, render_template, Response, send_file
from camera import Camera
from subprocess import Popen, PIPE
app = Flask(__name__)

# Start controller process
controller = Popen("python controller.py", stdin=PIPE, stdout=PIPE)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera')
def camera():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rotate', methods=['POST'])
def rotate():
    rotation = bytes("rotate="+request.form['rotation'], 'utf-8')
    controller.stdin.write(rotation)
    return 'OK'

@app.route('/sweep', methods=['POST'])
def sweep():
    controller.stdin.write(b'sweep')
    return 'OK'
