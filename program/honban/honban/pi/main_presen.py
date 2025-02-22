#raspberry pi 全体動作メインプログラム
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
from send import get
from test import test_get


def main_presen():
    ser_esp = serial.Serial(config.ESP_PORT, config.BAUDRATE)
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
    time.sleep(2)

    serial_rc(ser_esp, ser_pico)
"""
    while True:
        serial_rc(ser_esp, ser_pico)
        test_get()
"""
#実行
main_presen()

