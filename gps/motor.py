from RPi import GPIO
from time import sleep

class Motor():
    def __init__(self, pwm_pin, dir_pin):
        GPIO.setup(pwm_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        self.pwmPin = GPIO.PWM(pwm_pin, 1000)
        self.dirPin = dir_pin
    def setSpeed(self, speed):
        # set speed of motor
        self.pwmPin.ChangeDutyCycle(abs(speed))
        if (speed > 0):
            self.dirPin = GPIO.HIGH
        else:
            self.dirPin = GPIO.LOW
        pass

def motorTest(motor: Motor):
    motor.setSpeed(50)

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    motor = Motor(12,11)
    motorTest(motor)
