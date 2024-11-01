import serial
import time

# シリアルポートを設定 (例: /dev/ttyUSB0 または /dev/ttyACM0)
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # シリアル通信の準備のため少し待機

while True:
    if ser.in_waiting > 0:
        # 配列サイズを取得
        data_size = ser.read(1)
        data_size = int.from_bytes(data_size, "little")
        
        # データを受信
        data_array = []
        for i in range(data_size):
            data = ser.read(1)
            data_array.append(int.from_bytes(data, "little"))
        
        print("受信した配列:", data_array)
