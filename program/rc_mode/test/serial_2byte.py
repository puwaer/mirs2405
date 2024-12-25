import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # シリアル通信の初期化待ち

while True:
    if ser.in_waiting >= 12:  # 6つのデータ × 2バイト = 12バイト
        data = ser.read(12)  # 12バイトを一度に受信
        input_values = []

        # 2バイトごとに組み合わせてintに変換
        for i in range(0, 12, 2):
            pulse_value = data[i] | (data[i + 1] << 8)
            input_values.append(pulse_value)
        
        print("Received input values:", input_values)
