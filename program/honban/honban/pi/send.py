import serial
import time
import config
import struct

#pico
#角度送信
def send_angle(data, ser_pico):

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

def receive_get(ser_pico):

    data = [6, 0, 0, 0, 0, 0, 0]    #識別番号
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
        time.sleep(0.1)


    return pr_state  # 受信したデータを返す

def get(ser_pico, ser_arduino):
    data = [6, 0, 0, 0, 0, 0 ,0]    #配布物を取得
    send_angle(data, ser_pico)
    check_get = receive_get(ser_pico)
    data = [6, 1, 0, 0, 0, 0, 0]
    send_angle(data, ser_arduino)

    
'''
#走行命令の送信
def send_run(){
        time.sleep(2)  # シリアル通信の初期化待ち
    data = [2, 0, 0, 0, 0, 0, 0]

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

    ser_pico.close()
}
'''

#arduino
