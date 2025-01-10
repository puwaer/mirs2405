import socket
import json
import re

# Define file paths
OUTPUT_FILE_1 = './output/output_zed.json'
OUTPUT_FILE_2 = './output/output_head_depth.json'
OUTPUT_FILE_3 = './output/output_foot_depth.json'

# Counter for tracking file rotation
receive_counter = 0

def get_dict_data(sock):
    data = sock.recv(1024).decode('utf-8')  # 受信データをデコード
    #print(data)  # 受信データを表示
    
    # 制御文字や不要な部分を除去
    clean_data = re.sub(r'[^\d]', '', data)  # 数字以外を削除
    return clean_data

def get_output_filepath():
    global receive_counter
    receive_counter += 1
    
    # Rotate between files using modulo
    file_number = (receive_counter - 1) % 3 + 1
    
    if file_number == 1:
        return OUTPUT_FILE_1
    elif file_number == 2:
        return OUTPUT_FILE_2
    else:
        return OUTPUT_FILE_3

def get_data(HOST, PORT):
    while True:
        try:
            # ソケット接続
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            # データを受信して表示
            received_data = get_dict_data(sock)
            int_data = int(received_data)

            print(int_data)

            # 受信処理部分で以下のように使用
            current_output_file = get_output_filepath()
            # ファイルへの保存処理
            with open(f'{current_output_file}', 'w') as json_file:
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
    get_data(HOST, PORT)