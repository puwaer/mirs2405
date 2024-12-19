import socket
import numpy as np
import struct

# サーバーのIPアドレスとポート番号を設定
server_ip = '172.25.13.157'  # サーバーのIPアドレス
server_port = 12345          # サーバーのポート番号

# 送信するNumPy配列を作成
array = np.array([1.5, 2.5, 3.5, 4.5, 5.5], dtype=np.float64)

# 配列をバイト列に変換
array_data = array.tobytes()

# 配列のサイズを送信
array_size = struct.pack('i', len(array_data))

# ソケットを作成し、サーバーに接続
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# サイズ情報を送信
client_socket.send(array_size)

# 配列データを送信
client_socket.send(array_data)

# サーバーからの応答を受信
response = client_socket.recv(1024)
print(f"Received from server: {response.decode()}")

# ソケットを閉じる
client_socket.close()
