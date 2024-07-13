import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)
data = 'dataだよ'
ser.open()

#送信側
def send(data):
    ser.write(data.encode())
    print(data)


#受信側
def reception():
    string_data = ser.read()
    print(string_data)
    return string_data

