import socketserver
import sys
import json

HOST = "172.25.16.100"  
PORT = 5569

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            # 送信したい辞書データを作成
            data_dict = {
                'sensor1': 25.4,
                'sensor2': 30.1,
                'sensor3': 15.8
            }
            
            # 辞書をJSON文字列に変換
            json_str = json.dumps(data_dict)
            
            # 文字列をバイト列に変換
            data = json_str.encode('utf-8')
            
            # データサイズを取得
            size = len(data).to_bytes(4, byteorder='big')
            
            # サイズとデータを送信
            self.request.sendall(size + data)

socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer((HOST, PORT), TCPHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit()