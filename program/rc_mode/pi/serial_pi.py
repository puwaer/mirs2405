import serial
import struct
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

# 受信する変数を定義
received_values = [0] * 6  # 6つの要素を持つ配列を初期化
time.sleep(1)

while True:
    for i in range(6):
        if ser.in_waiting >= 4:  # 1つのintは4バイト
            int_bytes = ser.read(4)  # 4バイトを受信
            received_values[i] = struct.unpack('i', int_bytes)[0]  # intをデコード
            #print(f"Received value {i + 1}: {received_values[i]}")
            time.sleep(0.1)

    # 配列全体を表示
    print("Received values array:", received_values)
    time.sleep(0.1)  # 次の受信まで待機
