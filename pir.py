import time
import RPi.GPIO as GPIO
 
MONITOR_PIN = 18
 
class MotionSensor:

  def detect(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MONITOR_PIN, GPIO.IN)
    try:
      new = 1
      while True:
        old = new
        new = GPIO.input(MONITOR_PIN)
        #print(new, old)
        if old - new == 1:
          return True
        time.sleep(0.1)
    except KeyboardInterrupt:
      print('stop')
    finally:
      GPIO.cleanup()

if __name__ == "__main__":
  pir = MotionSensor()
  #pir.scan()
