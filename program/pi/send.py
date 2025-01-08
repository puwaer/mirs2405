import serial
import time
import config
import struct

'''
#jetsonデータ送信
def send_array(port: str, baudrate: int, array: list):
    """
    要素2の配列をシリアル通信で送信する関数

    Args:
        port (str): シリアルポート名 (例: "/dev/ttyUSB0")
        baudrate (int): ボーレート
        array (list): 送信する2要素の配列 (例: [1234, 5678])
    """
    # シリアルポートを開く
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # 配列の要素を送信（int型2要素をバイナリ形式に変換）
        data = struct.pack('2i', array[0], array[1])
        ser.write(data)
        print(f"Sent: {array}")
'''


#pico
#角度送信
def send_angle(data):
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    time.sleep(2)  # シリアル通信の初期化待ち
    #data = [3, -20, -20, 0, 0, 0, 0]

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
