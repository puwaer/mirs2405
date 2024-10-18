#raspberry pi シリアル通信プログラム
import serial
import struct
import numpy as np
import config

def init_serial(port=config.port_jetson_to_pi, baudrate=config.BOUDRATE):
    """シリアル通信の初期化"""
    ser = serial.Serial(port, baudrate, timeout=1)
    return ser

def close_serial(ser):
    """シリアル通信を閉じる"""
    ser.close()

#jetson nano → raspberry pi
def receive_position(ser):
    """シリアル通信で送られてきた1次元行列（x, y, z座標）を受信"""
    position = struct.unpack('fff', ser.read(12))
    return np.array(position, dtype=np.float32)

#raspberry pi → pico
def send_position_angles(ser, position_angles):
    """xyz座標、第１、第３、第４関節回転角度を送信"""
    ser.write(struct.pack('fff', *position_angles))

#raspberry pi → arudino
def send_angles(ser, angles):
    """ターンテーブル回転角度、第２関節回転角度をシリアル送信"""
    ser.write(struct.pack('fff', *angles))
