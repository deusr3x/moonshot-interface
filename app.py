from flask import Flask, render_template, request, url_for, jsonify, Response
from board import SCL, SDA
from time import sleep
import sys
from camera_pi import Camera
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

servo0 = servo.Servo(pca.channels[0], min_pulse=600, max_pulse=2400)

currentAngle = 0
app = Flask(__name__)

def SetAngle(delta):
    global currentAngle
    angle = currentAngle + delta
    if angle <= 0:
        angle = 0
    elif angle >= 180:
        angle = 180
    servo0.angle = angle
    currentAngle = angle

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
        #SetAngle(0)
    elif direction['payload'] == 'right':
        SetAngle(15)
        #SetAngle(180)
    else:
        pass

    return jsonify(data=currentAngle)

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        SetAngle(0) # set to middle
        app.run(host='0.0.0.0',port=8080, threaded=True)
    finally:
        #pwm.stop()
        #GPIO.cleanup()
        pca.deinit()
        sys.exit()
