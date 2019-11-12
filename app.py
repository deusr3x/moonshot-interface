from flask import Flask, render_template, request, url_for, jsonify, Response
# import RPi.GPIO as GPIO
from time import sleep
import sys
# import picamera

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(3, GPIO.OUT)

# pwm = GPIO.PWM(3, 50)
# pwm.start(0)

# cam = picamera.PiCamera()
# cam.resolution = (640, 480)

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
    print(duty)
#     GPIO.output(3, True)
#     pwm.ChangeDutyCycle(duty)
#     sleep(1)
#     GPIO.output(3,False)
#     pwm.ChangeDutyCycle(0)

def gen():
    while True:
        # cam.capture('image.jpg')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('image.jpg','rb').read() + b'\r\n')
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/horizontal', methods=['POST'])
def move_dir():
    direction = request.get_json(force=True)
    print(direction)
    if direction['payload'] == 'left':
        SetAngle(-15)
    elif direction['payload'] == 'right':
        SetAngle(15)
    else:
        pass
    
    # SetAngle(angle)
    global currentAngle
    return jsonify(data=currentAngle)

@app.route('/video_feed')
def video_feed():
   return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        # SetAngle(0)
        app.run(host='0.0.0.0',port=8080, threaded=True)
    except (KeyboardInterrupt, SystemExit):
        print("Goodbye")
        # pwm.stop()
        # GPIO.cleanup()
        sys.exit()
