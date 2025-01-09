import socket
import json
import re

def get_dict_data(sock):
    data = sock.recv(1024).decode('utf-8')  # 受信データをデコード
    #print(data)  # 受信データを表示
    
    # 制御文字や不要な部分を除去
    clean_data = re.sub(r'[^\d]', '', data)  # 数字以外を削除
    return clean_data

def get_data(HOST, PORT, output_file):
    while True:
        try:
            # ソケット接続
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            # データを受信して表示
            received_data = get_dict_data(sock)
            int_data = int(received_data)
            print(int_data)

            # Save int_data to a JSON file
            with open(f'{output_file}', 'w') as json_file:
                json.dump(int_data, json_file)

            # 接続を閉じる
            sock.close()
            
        except KeyboardInterrupt:
            print("\nClosing connection...")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            sock.close()
            continue

if __name__ == "__main__":
    HOST = '172.25.15.27'
    PORT = 5700
    output_file = './program/output/output_zed.json'
    get_data(HOST, PORT, output_file)