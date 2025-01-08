import socketserver
import sys
import json
import time

HOST = "172.25.15.27"  
PORT = 5700

class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.data_dict = server.data_dict
        self.counter = 0
        super().__init__(request, client_address, server)
        
    def handle(self):
        while True:
            try:
                
                # 辞書をJSON文字列に変換
                json_str = json.dumps(self.data_dict)
                
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

class CustomTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, data_dict, bind_and_activate=True):
        self.data_dict = data_dict
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

if __name__ == "__main__":
    # 送信したい辞書データを作成
    data_dict = {
        'sensor1': 25.4,
        'sensor2': 30.1,
        'sensor3': 15.8,
        }
    
    socketserver.TCPServer.allow_reuse_address = True
    server = CustomTCPServer((HOST, PORT), TCPHandler, data_dict=data_dict)

    try:
        print("Server started, waiting for connections...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
        sys.exit()