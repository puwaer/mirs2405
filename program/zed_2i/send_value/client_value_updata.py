import socket
import json

def get_dict_data(sock):
    data = sock.recv(1024).decode('utf-8')  # 受信データをデコード
    print("Raw received data:", data)  # 受信データを表示
    try:
        data_dict = json.loads(data)  # JSON文字列を辞書に変換
        return data_dict.get('message', '')  # messageキーの値を取得
    except json.JSONDecodeError:
        #print("Received data is not valid JSON")
        return None

if __name__ == "__main__":
    HOST = '172.25.15.27'
    PORT = 5700
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