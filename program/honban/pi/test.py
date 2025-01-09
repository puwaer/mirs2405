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
from receive import receive_pr
from receive import serial_rc
from receive import receive_distance
from receive import judge_angle
from send import send_angle


#身長から角度決定
hight = read_json_name(2)
print(hight)
angle = judge_angle(hight)
print(angle)



'''
#rc操作
def test_rc():
    serial_rc(ser_esp, ser_pico, ser_arduino)
test_rc()
'''

'''
#角度送信
def test_angle():
    data = [3, 10, -10, 0, 0, 0, 0]
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
