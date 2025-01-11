import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp
import socketserver
from typing import Tuple, Optional
import sys

class HeightMeasurementServer(socketserver.BaseRequestHandler):
    def setup(self):
        """Initialize the height measurement system when a client connects"""
        self.height_measurement = HeightMeasurement()
        if not self.height_measurement.open_camera():
            raise RuntimeError("Failed to initialize camera")
        print("Camera initialized successfully")

    def handle(self):
        """Handle client connection and stream height measurement data"""
        print(f"Client connected from {self.client_address}")
        try:
            while True:
                # Process frame and get height measurement
                height, frame = self.height_measurement.process_frame()
                
                if frame.size > 0:
                    # Encode frame for transmission
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    _, jpeg_data = cv2.imencode('.jpeg', frame, encode_param)
                    
                    # Prepare data packet with height information
                    frame_data = jpeg_data.tobytes()
                    height_data = str(height).encode() if height else b"None"
                    
                    # Create packet: [frame size (4 bytes)][height size (4 bytes)][height data][frame data]
                    frame_size = len(frame_data).to_bytes(4, byteorder='big')
                    height_size = len(height_data).to_bytes(4, byteorder='big')
                    packet = frame_size + height_size + height_data + frame_data
                    
                    # Send data
                    self.request.sendall(packet)
                
        except (ConnectionResetError, BrokenPipeError) as e:
            print(f"Client disconnected: {e}")
        finally:
            self.height_measurement.close()

    def finish(self):
        """Clean up when client disconnects"""
        if hasattr(self, 'height_measurement'):
            self.height_measurement.close()
        print(f"Client {self.client_address} disconnected")

class HeightMeasurement:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        
        # Initialize camera parameters
        self.init_params = sl.InitParameters()
        self.init_params.camera_resolution = sl.RESOLUTION.HD720
        self.init_params.depth_mode = sl.DEPTH_MODE.ULTRA
        
        # Initialize camera
        self.camera = sl.Camera()
        
        # Initialize image containers
        self.image = sl.Mat()
        self.depth = sl.Mat()
        self.point_cloud = sl.Mat()
        
        # Measurement parameters
        self.diff_rate = 1.15
        self.diff_const = 5

    # [Rest of the HeightMeasurement class remains unchanged]
    # ... [Previous methods remain exactly the same]

def main():
    HOST = "172.25.15.27"
    PORT = 5700
    
    # Enable address reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    # Create and start server
    try:
        server = socketserver.TCPServer((HOST, PORT), HeightMeasurementServer)
        print(f"Server started on {HOST}:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()