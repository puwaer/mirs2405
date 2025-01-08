import cv2
import sys
from zed_hight_class import HeightMeasurement
from server_value_updata import socketserver
from server_value_updata import CustomTCPServer
from server_value_updata import TCPHandler


HOST = "172.25.15.27"
PORT = 5700

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


def main_hight():
    height_measurement = HeightMeasurement()
    
    if not height_measurement.open_camera():
        return
    
    print("測定を開始します。'q'で終了します")
    
    while True:
        height, image = height_measurement.process_frame()
        
        if image.size > 0:
            cv2.imshow("ZED Height Measurement", image)
        
        if height is not None:
            print(f"測定身長: {height:.2f} cm")
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    height_measurement.close()
    print("終了しました")

if __name__ == "__main__":
    main_hight()