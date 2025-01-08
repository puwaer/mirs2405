import socket
import json

HOST = "172.25.15.27"  
PORT = 5700

def get_dict_data(sock):
    # サイズを受信
    size_data = sock.recv(4)
    if not size_data:
        return None
    size = int.from_bytes(size_data, byteorder='big')
    
    # データを受信
    buf = b''
    while len(buf) < size:
        chunk = sock.recv(size - len(buf))
        if not chunk:
            return None
        buf += chunk
        
    # バイト列をJSONに変換して辞書型に戻す
    json_str = buf.decode('utf-8')
    data_dict = json.loads(json_str)
    return data_dict.get('message', '')  # messageキーの値を取得

if __name__ == "__main__":
    while True:
        try:
            # ソケット接続
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            # データを受信して表示
            received_data = get_dict_data(sock)
            if received_data is not None:
                print("Received:", received_data)
            
            # 接続を閉じる
            sock.close()
            
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            sock.close()
            continue