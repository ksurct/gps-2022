import serial
import json
from time import sleep

class SerialInput(object):
    
    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
        self.ser.flush()
        self.fr_data = ""
        self.fl_data = ""
        self.f_data = ""
        self.l_data = ""
        self.r_data = ""
        self.course = ""
        self.longitude = ""
        self.latitude = ""
        self.altitude = ""
        self.speed = ""
        self.accelX= ""
        self.accelY= ""
        self.accelZ= ""
        self.magX = ""
        self.magY = ""
        self.magZ = ""

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
        return self.accelX

    def getAccelY(self):
        return self.accelY

    def getAccelZ(self):
        return self.accelZ

    def getMag(self):
        return [self.magX, self.magY, self.magZ]

if __name__ == '__main__':
    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    # ser.flush()
    ser = SerialInput()

    while True:
        ser.receiveData()
        sleep(1)
