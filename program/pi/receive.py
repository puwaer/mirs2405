import serial
import time
import send

#jetson
#def receive_position():

import socket
import numpy as np
import struct

def receive_camera(server_ip: str, server_port: int):
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
        print(f"Receiving array of size: {array_size} bytes")

        # 配列データを受信
        array_data = b""
        while len(array_data) < array_size:
            packet = client_socket.recv(1024)
            if not packet:
                raise ValueError("Connection closed before receiving all data.")
            array_data += packet

        # バイトデータをNumPy配列に変換
        array = np.frombuffer(array_data, dtype=np.float64)
        print(f"Received array: {array}")

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


camera_data = receive_camera('0.0.0.0', 12340)
if camera_data is not None:
    print(f"Processed array: {camera_data}")
else:
    print("No array received.")


#pico

def serial_rc(receive_port='/dev/ttyACM0', forward_port='/dev/ttyACM0', baudrate=115200):
    """
    シリアルポートでデータを受信し、他のポートにそのまま転送する関数。
    """
    # シリアル通信の初期化
    ser_receive = serial.Serial(receive_port, baudrate)
    ser_forward = serial.Serial(forward_port, baudrate)
    time.sleep(2)  # シリアル通信の初期化待ち

    try:
        while True:
            # データが一定以上たまっている場合に受信
            if ser_receive.in_waiting >= 10:  # 10バイト以上のデータが待機中か確認
                data = ser_receive.read(10)  # 10バイトを一度に受信
                input_values = []

                # 2バイトごとに組み合わせてintに変換
                for i in range(0, len(data), 2):  # len(data)を使って、データ長に依存する
                    pulse_value = data[i] | (data[i + 1] << 8)
                    input_values.append(pulse_value)
                
                # 転送データをそのまま送信
                ser_forward.write(data)

                print("Received input values:", input_values)
                
                # 特定の条件が満たされたらループを終了
                if len(input_values) > 4 and input_values[4] == 1:  # input_valuesの長さをチェック
                    print("Terminating based on received signal.")
                    break

    except serial.SerialException as e:
        # シリアル通信エラーの処理
        print(f"Serial communication error: {e}")
    except Exception as e:
        # その他のエラーの処理
        print(f"An unexpected error occurred: {e}")
    finally:
        # シリアルポートを閉じる
        ser_receive.close()
        ser_forward.close()

def receive_pr():
    size = 5  # 配列のサイズ
    bytes_per_value = 2  # 各値は2バイト
    total_bytes = size * bytes_per_value

    ser = serial.Serial('/dev/ttyACM0', 115200)
    time.sleep(2)  # シリアル通信の初期化待ち

    ft_state = []  # 受信したデータを格納するリスト

    while True:
        # データが十分に待機しているか確認
        if ser.in_waiting >= total_bytes:
            data = ser.read(total_bytes)  # 配列データを取得

            # データを2バイトずつ整数に変換
            for i in range(0, total_bytes, 2):
                pulse_value = data[i] | (data[i + 1] << 8)
                input_values.append(pulse_value)

            print("Received input values:", ft_state)
            break  # 受信後はループを抜ける

        # データがまだ受信されていない場合は、ループを続ける
        print("Waiting for data...")

    ser.close()  # シリアルポートを閉じる
    return pr_state  # 受信したデータを返す


#arduino





