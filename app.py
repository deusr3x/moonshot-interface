from flask import Flask, render_template, request, url_for, jsonify, Response
import RPi.GPIO as GPIO
from time import sleep
import sys
from camera_pi import Camera

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 50)
pwm.start(0)

currentAngle = 0
app = Flask(__name__)

def SetAngle(delta):
    global currentAngle
    angle = currentAngle + delta
    if angle <= 30:
        currentAngle = 30
    elif angle >= 120:
        currentAngle = 120
    else:
        currentAngle = angle
    duty = currentAngle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/horizontal', methods=['POST'])
def move_dir():
    global currentAngle
    direction = request.get_json(force=True)
    print(direction)
    if direction['payload'] == 'left':
        SetAngle(-15)
    elif direction['payload'] == 'right':
        SetAngle(15)
    else:
        pass
    
    return jsonify(data=currentAngle)

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        SetAngle(90) # set to middle
        app.run(host='0.0.0.0',port=8080, threaded=True)
    finally:
        pwm.stop()
        GPIO.cleanup()
        sys.exit()
