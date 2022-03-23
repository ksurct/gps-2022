
from RPi import GPIO
from time import sleep

class Motor():
    def __init__(self, pwm_pin, dir_pin):
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        self.pwmPin = GPIO.PWM(pwm_pin, 1000)
        self.dirPin = dir_pin
        GPIO.output(self.dirPin, GPIO.HIGH)
        self.pwmPin.start(0)
    def setSpeed(self, speed):
        # set speed of motor
        self.pwmPin.ChangeDutyCycle(abs(speed))
        if (speed > 0):
            GPIO.output(self.dirPin, GPIO.HIGH)
        else:
            GPIO.output(self.dirPin, GPIO.LOW)
    
    
if __name__ == "__main__":
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    motor = Motor(13,24)
    motor2 = Motor(12,23)
    motor.setSpeed(0)
    motor2.setSpeed(50)
    print("onward")
    sleep(2)
    motor.setSpeed(0)
    motor2.setSpeed(0)
    GPIO.cleanup()
