import socket
import json
import re

def get_dict_data(sock):
    data = sock.recv(1024).decode('utf-8')  # 受信データをデコード
    #print(data)  # 受信データを表示
    
    # 制御文字や不要な部分を除去
    #clean_data = re.sub(r'[^\d]', '', data)  # 数字以外を削除
    return data

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
            int_data = int(received_data)
            print(int_data)
            
            
            # 接続を閉じる
            sock.close()
            
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            sock.close()
            continue