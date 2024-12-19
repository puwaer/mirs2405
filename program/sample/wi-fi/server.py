import socket
import numpy as np
import struct

# サーバーのIPアドレスとポート番号を設定
server_ip = '0.0.0.0'  # すべてのインターフェースで待機
server_port = 12345     # 任意のポート番号

# ソケットを作成し、バインド
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# クライアントからの接続を待機
server_socket.listen(1)
print(f"Waiting for a connection on {server_ip}:{server_port}...")

# クライアント接続の待機
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# 配列のサイズを受信
array_size_data = client_socket.recv(4)
array_size = struct.unpack('i', array_size_data)[0]  # 配列のサイズ

# 配列のデータを受信
array_data = b""
while len(array_data) < array_size:
    array_data += client_socket.recv(1024)

# バイトデータをNumPy配列に変換
array = np.frombuffer(array_data, dtype=np.float64)  # 受信するデータの型に合わせる
print(f"Received array: {array}")

# 応答メッセージをクライアントに送信
client_socket.send("Array received!".encode())

# ソケットを閉じる
client_socket.close()
server_socket.close()
