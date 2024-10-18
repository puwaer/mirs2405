#jetson nano → raspberry pi シリアル通信（jetson nano 側）

import serial
import numpy as np
import struct

def init_serial(port='/dev/ttyUSB0', baudrate=9600):
    """シリアル通信の初期化"""
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser

def send_xyz(ser, position):
    """x, y, z座標をシリアル送信"""
    ser.write(struct.pack('fff', *position))

def close_serial(ser):
    """シリアル通信を閉じる"""
    ser.close()
