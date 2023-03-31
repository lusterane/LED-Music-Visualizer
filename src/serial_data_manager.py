import serial
import time
class Serial_Data_Manager():
    def __init__(self):
        self.arduino = serial.Serial(port='COM3', baudrate=250000 , timeout=.1)
        self.runtime = 1
    def write(self,x):
        self.arduino.write(x.encode())

    def send_power(self, x):
        self.arduino.write((str(x)+'\n').encode())
    def write_test(self):
        num = '23'
        self.arduino.write(num.encode())
        time.sleep(6)
        msg = self.arduino.read(self.arduino.inWaiting())
        print("Arduino:",msg)
    def write_read_test(self, x):
        self.arduino.write(x)
        time.sleep(0.05)
        data = self.arduino.read()
        return data
    def read_test(self):
        return self.arduino.readline()
    def convert_rgb_power_to_string(self,rgb,power):
        r,g,b = rgb
        ret_str = ''
        ret_str += self.__convert_int_to_string(r)
        ret_str += self.__convert_int_to_string(g)
        ret_str += self.__convert_int_to_string(b)
        ret_str += self.__convert_int_to_string(power)
        return ret_str

    def convert_power_to_string(self,power):
        return self.__convert_int_to_string(power)
    def __convert_int_to_string(self,val):
        if val < 10:
            return '00'+str(val)
        elif val < 100:
            return '0'+str(val)
        return str(val)

