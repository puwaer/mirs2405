import serial
import time

# シリアル通信の設定（適切なポートとボーレートを設定してください）
ser = serial.Serial('/dev/ttyACM0', 115200)  # Arduinoのポートに置き換えてください

while True:
    # 送信する配列
    data = [0, -30, -80, 60, -30]

    # 配列の各値を2バイト（上位バイト、下位バイト）に分けて送信
    for number in data:
        # 負の値を16ビットの符号付き整数として処理
        if number < 0:
            number += 2**16  # 2バイト範囲に収めるために16ビットの補数表現に変換

        high_byte = (number >> 8) & 0xFF  # 上位バイト
        low_byte = number & 0xFF         # 下位バイト
    
        ser.write(bytes([high_byte, low_byte]))  # 上位バイトと下位バイトを送信
    
        time.sleep(0.1)  # 少し待機

    # 終了シンボル（0xFFFF）を送信
    #ser.write(bytes([0xFF, 0xFF]))
    time.sleep(1)  # Arduinoがデータを受信するまで待機

# シリアル通信終了
# ser.close()  # 必要に応じて通信終了