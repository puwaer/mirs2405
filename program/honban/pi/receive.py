import serial
import time
import config
import socket
import numpy as np
import struct

#esp
#ラジコン通信
def serial_rc():   
     # シリアル通信の初期化
    ser_esp = serial.Serial(config.ESP_PORT, config.BAUDRATE)
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    #ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
    time.sleep(0.1)  # シリアル通信の初期化待ち
    data = [4, 0, 0, 0, 0, 0, 0]    #識別番号（ラジコンモードは4）
    size=14

    byte_array = bytearray()
    for value in data:
        # 符号付き16ビット整数の範囲をチェック
        if -0x8000 <= value <= 0x7FFF:
            # 16ビット内に収める (2の補数形式)
            value = value & 0xFFFF
            
            # 上位バイトと下位バイトに分割
            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF
            
            # バイト列に追加
            byte_array.append(low_byte)
            byte_array.append(high_byte)

        ser_esp.write(byte_array)   #識別番号を送信
        time.sleep(0.1)  # 少し待機

    while True:
        # ESP32からデータ受信
        if ser_esp.in_waiting >= size:  # 14バイト以上のデータが待機中か確認
            data = ser_esp.read(size)  # 14バイトを一度に受信
            input_values = []


            # 2バイトごとに組み合わせてintに変換
            for i in range(0, len(data), 2):
                pulse_value = data[i] | (data[i + 1] << 8)
                input_values.append(pulse_value)

            # データをPicoに転送
            ser_pico.write(data)

            # データをArduinoに転送
            #ser_arduino.write(data)

            print("Received input values:", input_values)

            # chGが押されたらラジコンモード終了
            if not(1040 <= input_values[5] <= 1100):
                print("Terminating based on received signal.")
                break

            time.sleep(0.2)


#pico
#フォトリフレクタ値を受信
def receive_pr(ser_pico):

    data = [1, 0, 0, 0, 0, 0, 0]    #識別番号
    size=14

    byte_array = bytearray()
    for value in data:
        # 符号付き16ビット整数の範囲をチェック
        if -0x8000 <= value <= 0x7FFF:
            # 16ビット内に収める (2の補数形式)
            value = value & 0xFFFF
            
            # 上位バイトと下位バイトに分割
            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF
            
            # バイト列に追加
            byte_array.append(low_byte)
            byte_array.append(high_byte)

        ser_pico.write(byte_array)
        time.sleep(0.1)  # 少し待機    

    while True:
        if ser_pico.in_waiting >= size:  # データが受信されているか確認
            data = ser_pico.read(size)  # 配列データを取得
            pr_state = []
            # データを2バイトずつ整数に変換
            for i in range(0, size, 2):
                pulse_value = data[i] | (data[i + 1] << 8)
                pr_state.append(pulse_value)

            print("Received input values:", pr_state)
            break  # データを受信したらループを抜ける

        # データがまだ受信されていない場合は、ループを続ける
        print("Waiting for data...")

    return pr_state  # 受信したデータを返す


def judge_angle(hight):
    joint1_angle = 25
    
    if hight <=110:
        angle=[3, joint1_angle, 89, 81, -180, 0, 0]
    elif 110 <= hight <=120:
        angle=[3, joint1_angle, 87, 93, -180, 0, 0]
    elif 120 <= hight <=130:
        angle=[3, joint1_angle, 86, 94, -180, 0, 0]
    elif 130 <= hight <=140:
        angle=[3, joint1_angle, 85, 95, -180, 0, 0]
    elif 140 <= hight <=150:
        angle=[3, joint1_angle, 83, 97, -180, 0, 0]
    elif 150 <= hight <=160:
        angle=[3, joint1_angle, 82, -82, -180, 0, 0]
    elif 160 <= hight <=170:
        angle=[3, joint1_angle, 81, -81, -180, 0, 0]
    elif 170 <= hight <=180:
        angle=[3, joint1_angle, 79, -79, -180, 0, 0]
    elif 180 <= hight <=190:
        angle=[3, joint1_angle, 78, -78, -180, 0, 0]
    elif 190 <= hight:
        angle=[3, joint1_angle, 76, -76, -180, 0, 0]

    return angle

#arduino

def receive_distance(ser_arduino):

    data = [10, 0, 0, 0, 0, 0, 0]    #識別番号
    size=14

    byte_array = bytearray()
    for value in data:
        # 符号付き16ビット整数の範囲をチェック
        if -0x8000 <= value <= 0x7FFF:
            # 16ビット内に収める (2の補数形式)
            value = value & 0xFFFF
            
            # 上位バイトと下位バイトに分割
            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF
            
            # バイト列に追加
            byte_array.append(low_byte)
            byte_array.append(high_byte)

        ser_arduino.write(byte_array)
        time.sleep(0.1)  # 少し待機    

    while True:
        if ser_arduino.in_waiting >= size:  # データが受信されているか確認
            data = ser_arduino.read(size)  # 配列データを取得
            distance = []
            # データを2バイトずつ整数に変換
            for i in range(0, size, 2):
                distance_value = data[i] | (data[i + 1] << 8)
                distance.append(distance_value)

            print("Received input values:", distance)
            break  # データを受信したらループを抜ける

        # データがまだ受信されていない場合は、ループを続ける
        #print("Waiting for data...")

    return distance  # 受信したデータを返す

