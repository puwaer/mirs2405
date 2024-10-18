#raspberry pi → pico シリアル通信（pico側）

import serial
import time
import struct
import numpy as np

def init_serial(port='/dev/ttyUSB0', baudrate=9600):
    """シリアル通信の初期化"""
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser

def receive_position(ser):
    """シリアル通信で送られてきた1次元行列（x, y, z座標、アーム第1、第３、第４関節回転角度）を受信"""
    position_angles = struct.unpack('fff', ser.read(12))
    return np.array(position_angles, dtype=np.float32)

def close_serial(ser):
    """シリアル通信を閉じる"""
    ser.close()
