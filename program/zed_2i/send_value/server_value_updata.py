import socketserver
import sys
import json

HOST = "172.25.14.19"
PORT = 5700

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # 辞書をJSON文字列に変換
            json_str = json.dumps(self.server.current_data)
            
            # 文字列をバイト列に変換
            data = json_str.encode('utf-8')
            
            # データサイズを取得
            size = len(data).to_bytes(4, byteorder='big')
            
            # サイズとデータを送信（1回だけ）
            self.request.sendall(size + data)
            
        except ConnectionError:
            print("Connection lost")
        except Exception as e:
            print(f"Error occurred: {e}")

class CustomTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.current_data = None
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


def main_server():
    socketserver.TCPServer.allow_reuse_address = True
    server = CustomTCPServer((HOST, PORT), TCPHandler)

    try:
        print("Server started")
        while True:
            # 入力を受け付ける
            input_text = input("Please enter the data you want to send: ")
            
            # 入力されたデータを保存
            server.current_data = input_text
            
            # クライアントからの接続を1回待ち受ける
            server.handle_request()
            
            print("Data sent. Waiting for next input...")
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()
        sys.exit()

if __name__ == "__main__":
    main_server()