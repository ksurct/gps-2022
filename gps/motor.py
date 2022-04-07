
import RPi.GPIO as GPIO
from time import sleep

class Motor():
    def __init__(self, pwm_pin, dir_pin, mod=1):
        # GPIO.setmode(GPIO.BCM)
        self.mod = mod
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        self.pwmPin = GPIO.PWM(pwm_pin, 1000)
        self.dirPin = dir_pin
        GPIO.output(self.dirPin, GPIO.HIGH)
        self.pwmPin.start(0)

    def setSpeed(self, speed):
        # set speed of motor
        # print("set speed {} after mod {}".format(speed, self.mod * speed))
        self.pwmPin.ChangeDutyCycle(abs(speed*self.mod))
        if (speed > 0):
            GPIO.output(self.dirPin, GPIO.HIGH)
        else:
            GPIO.output(self.dirPin, GPIO.LOW)
    
if __name__ == "__main__":
    num = int(input("1:"))
    num2 = int(input("2:"))
    num3 = float(input("3:")) 
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    motor = Motor(13,24)
    motor2 = Motor(12,23)
    motor.setSpeed(num)
    motor2.setSpeed(num2)
    print("onward")
    sleep(num3)
    motor.setSpeed(0)
    motor2.setSpeed(0)
    GPIO.cleanup()
