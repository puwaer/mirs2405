#raspberry pi → pico シリアル通信（raspberry pi 側）

import serial
import time

def init_serial(port='/dev/ttyUSB0', baudrate=9600):
    """シリアルポートを初期化する関数"""
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # 接続が安定するまで待機
    return ser

def send_matrix(ser, matrix):
    """行列をシリアルで送信する関数"""
    # 行列を文字列に変換
    matrix_str = '\n'.join([' '.join(map(str, row)) for row in matrix]) + '\n'
    ser.write(matrix_str.encode('utf-8'))
    ser.flush()

def close_serial(ser):
    """シリアルポートをクローズする関数"""
    ser.close()
