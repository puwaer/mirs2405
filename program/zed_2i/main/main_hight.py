import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp
import socketserver
import json
from typing import Tuple, Optional
from zed_hight_class import HeightMeasurement
from server_value_updata import CustomTCPServer, TCPHandler

"""
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            json_str = json.dumps(self.server.current_data)
            data = json_str.encode('utf-8')
            size = len(data).to_bytes(4, byteorder='big')
            self.request.sendall(size + data)
        except ConnectionError:
            print("Connection lost")
        except Exception as e:
            print(f"Error occurred: {e}")

class CustomTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        self.current_data = None
        super().__init__(server_address, RequestHandlerClass)
"""

        
def main():
    HOST = "172.25.15.27"
    PORT = 5700
    
    height_measurement = HeightMeasurement()
    if not height_measurement.open_camera():
        return
        
    server = CustomTCPServer((HOST, PORT), TCPHandler)
    server.allow_reuse_address = True
    
    print("測定を開始します。'q'で終了します")
    
    try:
        while True:
            height, image = height_measurement.process_frame()
            
            if image.size > 0:
                cv2.imshow("ZED Height Measurement", image)
            
            if height is not None:
                print(f"測定身長: {height:.2f} cm")
                server.current_data = {"height": float(height)}
                server.handle_request()
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        height_measurement.close()
        server.server_close()
        print("終了しました")

if __name__ == "__main__":
    main()