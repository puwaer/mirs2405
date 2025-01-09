import socket
import json

def get_dict_data(sock):
    #data = sock.recv(1024).decode('utf-8')  # 受信データをデコード
    #print(data)  # 受信データを表示
    # 最初の4バイトを受信してサイズ情報を取得
    size_data = sock.recv(4)
    if len(size_data) < 4:
        raise ValueError("Failed to receive size information")
    size = int.from_bytes(size_data, byteorder='big')

    # サイズに基づいてデータを受信
    data = sock.recv(size).decode('utf-8')
    
    return data

if __name__ == "__main__":
    HOST = '172.25.15.27'
    #HOST = '172.25.15.130'
    PORT = 5700
    while True:
        received_data_int = 0
        try:
            # ソケット接続
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            # データを受信して表示
            received_data = get_dict_data(sock)
            received_data_int = int(json.loads(received_data))
            if (received_data_int != 0):
                print(received_data_int)
                received_data_int = 0
                break
            # 接続を閉じる
            sock.close()
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            sock.close()
            continue
        