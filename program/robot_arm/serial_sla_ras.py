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
