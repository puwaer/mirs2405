import socket
import numpy as np
import struct

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


received_array = receive_array_once('0.0.0.0', 12340)
if received_array is not None:
    print(f"Processed array: {received_array}")
else:
    print("No array received.")
