import socket
import json

def connect_to_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # サーバーに接続
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            
            while True:
                try:
                    # データサイズを受信 (4バイト)
                    size_data = client_socket.recv(4)
                    if not size_data:
                        print("Server closed the connection.")
                        break
                    
                    # データサイズを整数に変換
                    data_size = int.from_bytes(size_data, byteorder='big')
                    
                    # 指定されたサイズ分のデータを受信
                    data = client_socket.recv(data_size)
                    if not data:
                        print("No data received.")
                        break
                    
                    # バイト列を文字列にデコード
                    json_str = data.decode('utf-8')
                    
                    # JSON文字列を辞書に変換
                    data_dict = json.loads(json_str)
                    
                    # 受信したデータを表示
                    print("Received data:", data_dict)
                
                except Exception as e:
                    print(f"Error occurred while receiving data: {e}")
                    break
    
    except ConnectionRefusedError:
        print(f"Could not connect to server at {host}:{port}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # サーバーのホストとポートを指定
    HOST = "127.25.15.27"  # サーバーのIPアドレス
    PORT = 5700        # サーバーのポート番号

    # サーバーに接続
    connect_to_server(HOST, PORT)
