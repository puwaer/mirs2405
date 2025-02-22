#raspberry pi 動作テスト用プログラム
import math
import numpy as np
import time
import serial
import sys
sys.path.append("./../zed")
import config
from read_json import read_json_name
#from inverse_kinematics import inverse_kinematics
from client_value_updata import get_camera
#from receive import receive_pr
from receive import serial_rc
from receive import test_rc
from receive import receive_distance
from receive import judge_angle
from send import send_angle
from send import receive_get

ser_esp = serial.Serial(config.ESP_PORT, config.BAUDRATE)
ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
time.sleep(2)

"""
while True:
    time.sleep(1)
    test_rc(ser_esp)
    print("finish")
"""



while True:
    test_rc(ser_esp)
    print("START")
    distance=read_json_name(0)
    hight=read_json_name(2)
    if distance<=100:
        time.sleep(1)
        data = [6, 0, 0, 0, 0, 0, 0]
        send_angle(data, ser_arduino)
        print("a")
        #data = [6, 0, 0, 0, 0, 0 ,0]    #配布物を取得
        data = judge_angle(hight)
        print(data)
        send_angle(data, ser_pico)
        print("aaa")
        receive_get(ser_pico)
        print("c")
        data = [6, 1, 0, 0, 0, 0, 0]
        send_angle(data, ser_arduino)
        print("d")
    time.sleep(5)


#time.sleep(1)
#serial_rc(ser_esp, ser_pico)
#print("finish")
#serial_rc()

#身長から角度決定
'''
hight = read_json_name(2)
print(hight)
arm_angle = judge_angle(hight)
print(arm_angle)
'''
'''
arm_angle = [3, 0, 0, 0, 0, 0, 0]
send_angle(arm_angle, ser_pico)
time.sleep(1)

'''
'''
arm_angle = [3, 0, 0, 0, 0, 0, 0]
send_angle(arm_angle, ser_pico)
time.sleep(1)
arm_angle = [3, 0, 10, 0, 0, 0, 0]
send_angle(arm_angle, ser_pico)
time.sleep(1)
arm_angle = [3, 0, -10, 0, 0, 0, 0]
send_angle(arm_angle, ser_pico)
time.sleep(1)
arm_angle = [3, 0, 0, 0, 0, 0, 0]
send_angle(arm_angle, ser_pico)
time.sleep(1)
'''

'''
#rc操作
def test_rc():
    serial_rc(ser_esp, ser_pico, ser_arduino)
test_rc()
'''

'''
#角度送信
def test_angle():
    data = [3, -10, 0, 0, 0, 0, 0]
    send_angle(data, ser_pico)
test_angle()
'''

'''
#フォトリフレクタ値の受信
def test_pr():
    print("Starting receive_pr...")
    pr_state = receive_pr(ser_pico)
    print(pr_state)
test_pr()
'''

def test_ar():
    data = [6, 1, 0, 0, 0, 0, 0]
    send_angle(data, ser_arduino)
    print("a")
    time.sleep(10)
    data = [6, 0, 0, 0, 0, 0, 0]
    send_angle(data, ser_arduino)
    print("b")
    time.sleep(10)

def test_get():
    time.sleep(1)
    data = [6, 0, 0, 0, 0, 0, 0]
    send_angle(data, ser_arduino)
    print("a")
    data = [6, 0, 0, 0, 0, 0 ,0]    #配布物を取得
    print("b")
    #send_angle(data, ser_pico)
    receive_get(ser_pico)
    print("c")
    data = [6, 1, 0, 0, 0, 0, 0]
    #send_angle(data, ser_arduino)
    print("d")

#test_ar()
#test_rc(ser_esp)
#print("start")
#test_get()
#receive_get(ser_pico)
#receive_get(ser_pico)
#data = [3, 0, 0, 0, 0, 0, 0]
#send_angle(data, ser_pico)

"""
head = read_json_name(0)
print(head)
foot = read_json_name(1)
print(foot)
hight = read_json_name(2)
print(hight)
"""

#while True:
    #serial_rc(ser_esp, ser_pico, ser_arduino)


#test_get()

