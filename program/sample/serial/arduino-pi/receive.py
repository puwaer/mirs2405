import serial
import time

def receive_data():
    size = 5  # 配列のサイズ
    bytes_per_value = 2  # 各値は2バイト
    total_bytes = size * bytes_per_value

    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)  # シリアル通信の初期化待ち

    while True:
        if ser.in_waiting >= (total_bytes + 2):  # スタートバイト + データ + エンドバイト
            # スタートバイトを探す
            if ser.read(1) == b'\xFF':  # スタートバイトが見つかるまで読み飛ばす
                data = ser.read(total_bytes)  # 配列データを取得
                if ser.read(1) == b'\xFE':  # エンドバイトを確認
                    input_values = []

                    # データを2バイトずつ整数に変換
                    for i in range(0, total_bytes, 2):
                        pulse_value = data[i] | (data[i + 1] << 8)
                        input_values.append(pulse_value)

                    print("Received input values:", input_values)


receive_data()
