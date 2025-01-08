import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp
import socketserver
import json
import math
from typing import Tuple, Optional
from zed_hight_class import HeightMeasurement
from server_value_updata import CustomTCPServer, TCPHandler


def main_height_server():
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
                print(f"height: {height:.2f} cm")

                if isinstance(height, (int, float)) and not (isinstance(height, float) and math.isnan(height)):
                    server.current_data = {"height": float(height)}
                    server.handle_request()
                else:
                    print("Error: height is not a number")


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        height_measurement.close()
        server.server_close()
        print("終了しました")



if __name__ == "__main__":
    main_height_server()