import socketserver
import sys
import json
import time

HOST = "172.25.16.100"  
PORT = 5700

class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.counter = 0
        super().__init__(*args, **kwargs)
        
    def handle(self):
        while True:
            try:
                # 送信したい辞書データを作成
                data_dict = {
                    'sensor1': 25.4,
                    'sensor2': 30.1,
                    'sensor3': 15.8,
                    'time': self.counter
                }
                
                # 辞書をJSON文字列に変換
                json_str = json.dumps(data_dict)
                
                # 文字列をバイト列に変換
                data = json_str.encode('utf-8')
                
                # データサイズを取得
                size = len(data).to_bytes(4, byteorder='big')
                
                # サイズとデータを送信
                self.request.sendall(size + data)
                
                self.counter += 1
                time.sleep(0.5)
                

            except ConnectionError:
                print("Connection lost")
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                break

socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer((HOST, PORT), TCPHandler)

try:
    print("Server started, waiting for connections...")
    server.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    server.shutdown()
    server.server_close()
    sys.exit()