import socket
import numpy as np
import struct
import time

def send_arrays_continuously(server_ip: str, server_port: int, array: np.ndarray):
    """
    サーバーに常に同じ配列を送り続けるクライアント関数。

    :param server_ip: サーバーのIPアドレス
    :param server_port: サーバーのポート番号
    :param array: 送信するNumPy配列
    """
    while True:
        try:
            # ソケットを作成し、サーバーに接続
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Attempting to connect to the server...")
            client_socket.connect((server_ip, server_port))
            print("Connected to the server!")

            while True:
                # 配列をバイト列に変換
                array_data = array.tobytes()

                # 配列のサイズを送信
                array_size = struct.pack('i', len(array_data))
                client_socket.sendall(array_size)

                # 配列データを送信
                client_socket.sendall(array_data)
                print(f"Sent array: {array}")

                # 一定時間待機して再送信
                time.sleep(1)

        except (ConnectionRefusedError, BrokenPipeError):
            print("Server not available or disconnected. Retrying in 2 seconds...")
            time.sleep(2)

        except KeyboardInterrupt:
            print("Stopping client.")
            break

        finally:
            # ソケットを閉じる
            client_socket.close()


constant_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
send_arrays_continuously('172.25.13.157', 12340, constant_array)
