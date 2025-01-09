import socket
import json
import struct

def receive_data(sock):
    try:
        # まずデータの長さ（4バイト）を受信
        length_bytes = sock.recv(4)
        if not length_bytes:
            return None
            
        # バイト列を整数に変換
        length = struct.unpack('!I', length_bytes)[0]
        
        # 実際のデータを受信
        data = b''
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                return None
            data += chunk
            
        # JSONデータをデコード
        json_data = data.decode('utf-8')
        result = json.loads(json_data)
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラー: {e}")
        return None
    except Exception as e:
        print(f"受信エラー: {e}")
        return None

if __name__ == "__main__":
    HOST = '172.25.15.27'  # サーバーのIPアドレスに合わせて変更
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
                    print(f"\n推定結果:")
                    print(f"年齢: {result['age']}")
                    print(f"性別: {result['gender']}")
                    print("-" * 20)
                
        except KeyboardInterrupt:
            print("\n接続を終了します...")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            sock.close()
            continue

        finally:
            sock.close()