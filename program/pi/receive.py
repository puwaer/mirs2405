import serial
import time
import config
import socket
import numpy as np
import struct

#jetson
def receive_array_once(server_ip: str, server_port: int):
    """
    クライアントから配列を1度だけ受信するサーバー関数。

    :param server_ip: サーバーのIPアドレス
    :param server_port: サーバーのポート番号
    :return: 受信したNumPy配列
    """
    try:
        # ソケットを作成し、サーバーに接続
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print(f"Waiting for a connection on {server_ip}:{server_port}...")

        # クライアント接続を受け付ける
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # 配列のサイズを受信
        array_size_data = client_socket.recv(4)
        if not array_size_data:
            raise ValueError("Failed to receive array size.")
        array_size = struct.unpack('i', array_size_data)[0]
        #print(f"Receiving array of size: {array_size} bytes")

        # 配列データを受信
        array_data = b""
        while len(array_data) < array_size:
            packet = client_socket.recv(1024)
            if not packet:
                raise ValueError("Connection closed before receiving all data.")
            array_data += packet

        # バイトデータをNumPy配列に変換
        array = np.frombuffer(array_data, dtype=np.int32)
        #print(f"Received array: {array}")

        # 応答メッセージをクライアントに送信
        client_socket.send("Array received!".encode())

        return array

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # クライアントソケットを閉じる
        client_socket.close()
        server_socket.close()


'''
#jetsonからのデータ取得
def receive_array(port: str, baudrate: int) -> list:
    """
    シリアル通信で受信したデータを2要素の配列として返す関数

    Args:
        port (str): シリアルポート名 (例: "/dev/ttyS0")
        baudrate (int): ボーレート

    Returns:
        list: 受信した2要素の配列 (例: [1234, 5678])
    """
    # シリアルポートを開く
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # 必要なバイト数が受信できるまで待つ
        while ser.in_waiting < 8:  # int型2要素 = 4バイト × 2 = 8バイト
            pass
        
        # 受信したデータを読み取る
        data = ser.read(8)
        # バイナリデータを解釈して配列に変換
        array = list(struct.unpack('2i', data))
        print(f"Received: {array}")
        return array
'''

#esp
#ラジコン通信
def serial_rc():   
     # シリアル通信の初期化
    ser_esp = serial.Serial(config.ESP_PORT, config.BAUDRATE)
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    #ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
    time.sleep(2)  # シリアル通信の初期化待ち
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

            # chEが押されたらラジコンモード終了
            if input_values[0] == 0:
                print("Terminating based on received signal.")
                break

            time.sleep(0.2)

   

    # シリアルポートを閉じる
    ser_esp.close()
    ser_pico.close()
    #ser_arduino.close()


#pico
#フォトリフレクタ値を受信
def receive_pr():
     # シリアル通信の初期化
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    time.sleep(2)  # シリアル通信の初期化待ち
    data = [2, 0, 0, 0, 0, 0, 0]    #識別番号
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

    ser_pico.close()  # シリアルポートを閉じる
    return pr_state  # 受信したデータを返す

def judge_angle(hight):
    if 100 <= hight <=110:
        angle=[3, 10, 10, 10, 0, 0, 0]
    elif 120 <= hight <=120:
        angle=[3, 20, 20, 20, 0, 0 ,0]
    elif 120 <= hight <=130:
        angle=[3, 30, 30, 30, 0, 0, 0]
    elif 130 <= hight <=140:
        angle=[3, 40, 40, 40, 0, 0, 0]
    elif 140 <= hight <=150:
        angle=[3, 50, 50, 50, 0, 0, 0]
    elif 150 <= hight <=160:
        angle=[3, 60, 60, 60, 0, 0 ,0]
    elif 160 <= hight <=170:
        angle=[3, 70, 70, 70, 0, 0, 0]
    elif 170 <= hight <=180:
        angle=[3, 80, 80, 80, 0, 0, 0]
    elif 180 <= hight <=190:
        angle=[3, 90, 90, 90, 0, 0, 0]

    return angle

#arduino

def receive_distance():
     # シリアル通信の初期化
    ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
    time.sleep(0.1)  # シリアル通信の初期化待ち
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

    ser_arduino.close()  # シリアルポートを閉じる
    return distance  # 受信したデータを返す

