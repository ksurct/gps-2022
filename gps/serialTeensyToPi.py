import serial
import json
from time import sleep

class SerialInput(object):
    
    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
        self.ser.flush()
        self.fr_data = -1
        self.fl_data = -1
        self.f_data = -1
        self.l_data = -1
        self.r_data = -1
        self.course = 0.0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.speed = 0.0
        self.accelX= 0.0
        self.accelY= 0.0
        self.accelZ= 0.0
        self.magX = 0.0
        self.magY = 0.0
        self.magZ = 0.0

    def receiveData(self):
        self.pingTeensy()
        line = json.loads(self.ser.readline().decode('utf-8').rstrip())
        # print(line)
        self.fr_data = line['fr_data']
        self.fl_data = line['fl_data']
        self.f_data = line['f_data']
        self.l_data = line['l_data']
        self.r_data = line['r_data']
        self.longitude = line['longitude']
        self.latitude = line['latitude']
        self.altitude = line['altitude']
        self.course = line['course']
        self.accelX = line['accelX']
        self.accelY = line['accelY']
        self.accelZ = line['accelZ']
        self.magZ = line['magX']
        self.magY = line['magY']
        self.magZ = line['magZ']
        
    def pingTeensy(self):
        self.ser.write(b'r')

    def getFrontRightSensorData(self):
        return self.fr_data
        
    def getFrontLeftSensorData(self):
        return self.fl_data
        
    def getFrontSensorData(self):
        return self.f_data
        
    def getLeftSensorData(self):
        return self.l_data
        
    def getRightSensorData(self):
        return self.r_data
        
    def getLongitude(self):
        return self.longitude
        
    def getLatitude(self):
        return self.latitude
        
    def getAltitude(self):
        return self.altitude
        
    def getCourse(self):
        return self.course

    def getAccelX(self):
        return float(self.accelX)

    def getAccelY(self):
        return float(self.accelY)

    def getAccelZ(self):
        return float(self.accelZ)

    def getMag(self):
        return [self.magX, self.magY, self.magZ]

if __name__ == '__main__':
    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    # ser.flush()
    ser = SerialInput()

    while True:
        ser.receiveData()
        sleep(1)
