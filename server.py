from flask import Flask, request, render_template
from subprocess import Popen, PIPE
app = Flask(__name__)

# Start controller process
controller = Popen("python controller.py", stdin=PIPE, stdout=PIPE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    pass
    #return Response()

@app.route('/rotate', methods=['POST'])
def rotate():
    rotation = bytes(request.form['rotation'], 'utf-8')
    controller.stdin.write(rotation)
    return 'OK'

@app.route('/sweep', methods=['POST'])
def sweep():
    controller.stdin.write(b'sweep')
    return 'OK'
