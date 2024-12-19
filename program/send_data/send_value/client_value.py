import socket
import json

HOST = "172.25.16.100"  
PORT = 5700

def get_dict_data(sock):
    # サイズを受信
    size = int.from_bytes(sock.recv(4), byteorder='big')
    
    # データを受信
    buf = b''
    while len(buf) < size:
        buf += sock.recv(size - len(buf))
        
    # バイト列をJSONに変換して辞書型に戻す
    json_str = buf.decode('utf-8')
    return json.loads(json_str)

# ソケット接続
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
    while True:
        # データを受信して表示
        received_data = get_dict_data(sock)
        print(received_data)  # または必要な処理を実行
        
except KeyboardInterrupt:
    print("\nClosing connection...")
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    sock.close()