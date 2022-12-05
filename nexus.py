#!/usr/bin/python3

# Copyright (c) 2022 Raspberry Pi Ltd
# Author: Alasdair Allan <alasdair@raspberrypi.com>
# SPDX-License-Identifier: BSD-3-Clause


import argparse
import os
import sys
import libcamera
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image, ImageDraw, ImageFont
from picamera2 import MappedArray, Picamera2, Preview

# For Webserver streaming mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
import io
import logging
import socketserver
from http import server
from threading import Condition, Thread
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# For managinfg the servos moving the camera
from gpiozero import Servo
import math
from time import sleep, time
from gpiozero.pins.pigpio import PiGPIOFactory
from motor import MotorController

# for distance sensors
import RPi.GPIO as GPIO

# For managing OLED screen
import spidev as SPI
# sys.path.append("LCD")
from LCD_1inch47 import LCD_1inch47

# OLED pins
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

# Initial Eyes values
vpos=86
EYE=50
PUPIL=20
TICK=1
EXR =80
EXL = 240
disp = LCD_1inch47()
disp.Init()
disp.clear()
image1 = Image.new("RGB", (disp.width,disp.height ), "BLACK")
draw = ImageDraw.Draw(image1)

# initial Servos values
factory = PiGPIOFactory()
servot = Servo(4, min_pulse_width=0.7/1000, max_pulse_width=1.9/1000, pin_factory=factory)
servod = Servo(17, min_pulse_width=0.4/1000, max_pulse_width=2.4/1000, pin_factory=factory)
horiz = 180
vert = 180
mot = MotorController()

# initiate sensors

#GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 26 #37
PIN0_ECHO = 22 #15
PIN1_ECHO = 23 #16
PIN2_ECHO = 6 #31
PIN3_ECHO = 5 #29

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN0_ECHO, GPIO.IN)
GPIO.setup(PIN1_ECHO, GPIO.IN)
GPIO.setup(PIN2_ECHO, GPIO.IN)
GPIO.setup(PIN3_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)
print ("Waiting for sensor to settle")
sleep(2)

# Initiate webpage
PAGE = """\
<html>
<head>
<title>NEXUS Realtime Streaming</title>
</head>
<body>
<h1>NEXUS Streaming Demo</h1>
<img src="stream.mjpg" width="800" height="600" />
</body>
</html>
"""

normalSize = (800, 600)
lowresSize = (400, 300)
rectangles = []

picam2 = Picamera2()

# Eyes functions
def circle(x,y,r,c):
    draw.ellipse((y-r,x-r+7,y+r,x+r-7), fill = (c*255,c*255,255))

def drawEyes(plh,prh,plv):
    circle(EXR, vpos, EYE, 1)
    circle(EXL, vpos, EYE, 1)
    circle(EXR+plh, vpos+plv, PUPIL, 0)
    circle(EXL+prh, vpos+plv, PUPIL, 0)
    disp.ShowImage(image1)

def centerDraw():
    drawEyes(7,-7,0)

def look_center():
    centerDraw()

def look_left():
    drawEyes(-20,-20,0)

def look_up():
    drawEyes(7,-7,-20)

def look_down():
    drawEyes(7,-7,+20)

def look_right():
    drawEyes(20,20,0)

# function for calculating sensors distance

def distance (pin):
    new_reading = False
    counter = 0

    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    sleep(0.01)
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(pin)==0:
        pass
        counter += 1
        if counter == 5000:
            new_reading == True
            break
    pulse_start_time = time()

    if new_reading:
        return False

    while GPIO.input(pin)==1:
        pass
    pulse_end_time = time()

    pulse_duration = pulse_end_time - pulse_start_time
    return round(pulse_duration * 17150, 2)


def distance_front():


    sleft = distance(PIN0_ECHO)
    print ("Distance Left:", sleft, "cm", end=" | ")

    sright = distance(PIN1_ECHO)
    print ("Distance Right:", sright, "cm", end=" | ")

    scenter = distance(PIN2_ECHO)
    print ("Distance Center:",scenter,"cm")

    return sleft, sright, scenter

def distance_back():

    sback = distance(PIN3_ECHO)
    print ("Distance Back:", sback, "cm")

    return sback

# Class for image streaming

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def head(vertical, horizontal):
        servot.value = math.sin(math.radians(vertical))
        servod.value = math.sin(math.radians(horizontal))
        sleep(0.01)



def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def DrawRectangles(request):
    with MappedArray(request, "main") as m:
        for rect in rectangles:
          #  print(rect)
            rect_start = (int(rect[0] * 2) - 5, int(rect[1] * 2) - 5)
            rect_end = (int(rect[2] * 2) + 5, int(rect[3] * 2) + 5)
            cv2.rectangle(m.array, rect_start, rect_end, (0, 255, 0, 0))
            if len(rect) == 5:
                text = rect[4]
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(m.array, text, (int(rect[0] * 2) + 10, int(rect[1] * 2) + 10), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

############################
# MAIN LOOP LOGIC FUNCTION #
############################
def InferenceTensorFlow(image, model, output, label=None):
    global rectangles
    global horiz
    global vert
    global mot

    if label:
        labels = ReadLabelFile(label)
    else:
        labels = None

    interpreter = tflite.Interpreter(model_path=model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    floating_model = False
    if input_details[0]['dtype'] == np.float32:
        floating_model = True

    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    initial_h, initial_w, channels = rgb.shape

    picture = cv2.resize(rgb, (width, height))

    input_data = np.expand_dims(picture, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    detected_boxes = interpreter.get_tensor(output_details[0]['index'])
    detected_classes = interpreter.get_tensor(output_details[1]['index'])
    detected_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])

    rectangles = []
    person_score = 0
    person = []
    for i in range(int(num_boxes)):
        top, left, bottom, right = detected_boxes[0][i]
        classId = int(detected_classes[0][i])
        score = detected_scores[0][i]
        if score > 0.5:
            xmin = left * initial_w
            ymin = bottom * initial_h
            xmax = right * initial_w
            ymax = top * initial_h
            box = [xmin, ymin, xmax, ymax]
            rectangles.append(box)
            if labels:
                print(labels[classId], 'score = ', score)
                rectangles[-1].append(labels[classId])
                if labels[classId] == 'person' and score > person_score:
                   person = box
                   person_score = score
            else:
                print('score = ', score)

    if person_score > 0:
        person_width = person[2] - person[0]
        person_height = person[3] - person[1]
        person_middlex = person[0] + person_width // 2
        person_middley = person[1] + person_height // 2

        if (person_middlex - lowresSize[0] // 2) > lowresSize[0] //4:
            horiz -= 10
            look_left()
        elif (person_middlex - lowresSize[0] // 2) < -lowresSize[0] // 4:
            horiz += 10
            look_right()
        if (person_middley - lowresSize[1] // 2) > lowresSize[1] //4:
            vert -= 10
            look_down()
        elif (person_middley - lowresSize[1] // 2) < -lowresSize[1] // 4:
            vert += 10
            look_up()

        sf = 20
        if (person_width < (lowresSize[0] / 4)) and (person_height < (lowresSize[1] / 4)):
            sl,sr,sc = distance_front()
            if sc > sf and  sr > sf and sl > sf:
                mot.forward()
            else:
                mot.stop()
        elif (person_width > (lowresSize[0] / 2)) or (person_height > (lowresSize[1] / 2)):
            sb = distance_back()
            if sb > sf:
                mot.reverse()
            else:
                mot.stop()
        else:
            mot.stop()

        if horiz < 90:
            horiz = 90
        elif horiz > 270:
            horiz = 270

        if horiz < 160:
            mot.turn_l(duration=0.25)
            horiz=180
            look_center()
        elif horiz > 200:
            mot.turn_r(duration=0.25)
            horiz=180
            look_center()

        if vert < 90:
            vert = 90
        elif vert > 270:
            vert = 270

        head(vert, horiz)

    else:
        mot.stop()

def servidor():
    global output

    try:
        output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam2.stop_recording()

def main():
    output_file = 'out.jpg'
    label_file = 'coco_labels.txt'
    head(180,180)
    look_center()

    config = picam2.create_video_configuration(main={"size": normalSize},lores={"size": lowresSize, "format": "YUV420"},
                                               transform=libcamera.Transform(vflip=True))
    picam2.configure(config)

    stride = picam2.stream_configuration("lores")["stride"]
    picam2.post_callback = DrawRectangles

    t=Thread(target=servidor)
    t.daemon=True
    t.start()

    try:
        while True:
            buffer = picam2.capture_buffer("lores")
            grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
            result = InferenceTensorFlow(grey, "mobilenet_v2.tflite", output_file, label_file)
    except KeyboardInterrupt:
        print('Bye Dave!')
        mot.stop()

if __name__ == '__main__':
    main()
