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

#jetson nano → raspberry pi シリアル通信（raspberry pi 側）

import serial

def receive_matrix(ser):
    """シリアルから行列を受信する関数"""
    received_data = ser.readline().decode('utf-8').strip()  # 1行読み取る
    matrix = []
    
    for line in received_data.split('\n'):
        row = list(map(int, line.split()))  # 行を整数のリストに変換
        matrix.append(row)
        
    return matrix

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # シリアルポートを設定
    while True:
        matrix = receive_matrix(ser)
        print("Received Matrix:", matrix)

if __name__ == "__main__":
    main()
