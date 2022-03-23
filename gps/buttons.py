
import signal
import sys
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

leds = [16, 20, 21, 18]

class Button:
    
    def __init__(self, pin, func):
        self.pin = pin
        self.func = func
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.RISING, 
            callback=self.callFunc, bouncetime=500)
        
    def getPin(self):
        return self.pin
    
    def callFunc(self, aux):
        self.func(self.getPin())
        
def f(pin):
    print(pin)
    
def reboot(aux):
    # robot.Reboot()
    for j in range(2):
        for i in range(5):
            if(not (i == 0)):
                GPIO.output(leds[i-1], GPIO.LOW)
            if(not (i == 4)):
                GPIO.output(leds[i], GPIO.HIGH)
            time.sleep(.05)
        
        for i in range(5):
            if(not (i == 0)):
                GPIO.output(leds[4-i], GPIO.LOW)
            if(not (i == 4)):
                GPIO.output(leds[3-i], GPIO.HIGH)
            time.sleep(.05)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
        
if __name__ == "__main__":
    
    GPIO.setmode(GPIO.BCM)
    b1 = Button(11, f) 
    b2 = Button(25, f) 
    b3 = Button(8, reboot) 
    b4 = Button(7, f)
    led1 = 16 # green
    led2 = 20 # red
    led3 = 21 # the weird orange one
    led4 = 18 # white
    
    
    #LEDs
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)
    GPIO.setup(led3, GPIO.OUT)
    GPIO.setup(led4, GPIO.OUT)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
    
    
    