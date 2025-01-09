import socket
import json

def receive_data(sock):
    try:
        data = sock.recv(1024).decode('utf-8')
        result = json.loads(data)
        return result
    except json.JSONDecodeError:
        print("JSONデコードエラー")
        return None
    except Exception as e:
        print(f"受信エラー: {e}")
        return None

if __name__ == "__main__":
    HOST = '172.25.15.27'
    PORT = 5700

    while True:
        try:
            # ソケット接続
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))

            while True:
                # データを受信して表示
                result = receive_data(sock)
                if result:
                    print(f"年齢: {result['age']}")
                    print(f"性別: {result['gender']}")
                    print("-------------------")
                
        except KeyboardInterrupt:
            print("\n接続を終了します...")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            sock.close()
            continue

        finally:
            sock.close()