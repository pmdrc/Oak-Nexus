import RPi.GPIO as GPIO
import time

try:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 7
      PIN_ECHO = 11
      PIN0_TRIGGER = 13
      PIN0_ECHO = 15

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)
      GPIO.setup(PIN0_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN0_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)
      GPIO.output(PIN0_TRIGGER, GPIO.LOW)

      print ("Waiting for sensor to settle")

      time.sleep(2)

      print ("Calculating distance")
      while True:

          GPIO.output(PIN_TRIGGER, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN_TRIGGER, GPIO.LOW)

          while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
          while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          distance = round(pulse_duration * 17150, 2)
          print ("Distance BACK:",distance,"cm")

          GPIO.output(PIN0_TRIGGER, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN0_TRIGGER, GPIO.LOW)

          while GPIO.input(PIN0_ECHO)==0:
                pulse_start_time = time.time()
          while GPIO.input(PIN0_ECHO)==1:
                pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          distance = round(pulse_duration * 17150, 2)
          print ("Distance FRONT:",distance,"cm")
          time.sleep(1)

except KeyboardInterrupt:
      GPIO.cleanup()
      print ("All Done")
