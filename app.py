from flask import Flask, render_template, request, url_for, jsonify, Response
import RPi.GPIO as GPIO
from time import sleep
import sys
from camera_pi import Camera

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 50)
pwm.start(0)

# cam = picamera.PiCamera()
# cam.resolution = (640, 480)

app = Flask(__name__)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)

def gen(camera):
    while True:
        # cam.capture('image.jpg')
        frame = camera.get_frame()
        #yield (b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + open('image.jpg','rb').read() + b'\r\n')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/degrees', methods=['POST'])
def degree():
    degrees = request.get_json(force=True)
    print(degrees)
    angle = int(degrees['payload'])
    SetAngle(angle)
    return '{data: 0}'

@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        SetAngle(0)
        app.run(host='0.0.0.0',port=8080, threaded=True)
    except (KeyboardInterrupt, SystemExit):
        print("Goodbye")
        pwm.stop()
        GPIO.cleanup()
        sys.exit()
    finally:
        pwm.stop()
        GPIO.cleanup()
        sys.exit()
