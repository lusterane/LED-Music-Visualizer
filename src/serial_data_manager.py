import serial
import time
class Serial_Data_Manager():
    def __init__(self):
        self.arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

    def write_read(self, x):
        self.arduino.write(x)
        time.sleep(0.05)
        data = self.arduino.read()
        return data
    def read(self):
        return self.arduino.readline()
    def write(self,x):
        s = str(x)
        self.arduino.write(s.encode())

    def send_power(self, x):
        self.arduino.write((str(x)+'\n').encode())
    def write_test(self):
        num = '23'
        self.arduino.write(num.encode())
        time.sleep(6)
        msg = self.arduino.read(self.arduino.inWaiting())
        print("Arduino:",msg)