import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp
import socketserver
import sys
from typing import Tuple, Optional

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
        
    def open_camera(self) -> bool:
        status = self.camera.open(self.init_params)
        if status != sl.ERROR_CODE.SUCCESS:
            print(f"Failed to open camera: {status}")
            return False
        return True

    def get_skeletal_points(self, image: np.ndarray) -> Tuple[Optional[tuple], Optional[tuple]]:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            head_point = (int(landmarks[self.mp_pose.PoseLandmark.NOSE].x * image.shape[1]),
                         int(landmarks[self.mp_pose.PoseLandmark.NOSE].y * image.shape[0]))
            foot_point = (int(landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * image.shape[1]),
                         int(landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * image.shape[0]))
            return head_point, foot_point
        return None, None

    def process_frame(self) -> Tuple[Optional[float], np.ndarray]:
        if self.camera.grab() != sl.ERROR_CODE.SUCCESS:
            return None, np.array([])

        self.camera.retrieve_image(self.image, sl.VIEW.LEFT)
        self.camera.retrieve_measure(self.depth, sl.MEASURE.DEPTH)
        self.camera.retrieve_measure(self.point_cloud, sl.MEASURE.XYZ)

        image_ocv = self.image.get_data()
        image_ocv = np.array(image_ocv, dtype=np.uint8)
        
        try:
            image_ocv = cv2.cvtColor(image_ocv, cv2.COLOR_RGBA2BGR)
        except cv2.error as e:
            print(f"Image conversion error: {e}")
            return None, image_ocv

        head_point, foot_point = self.get_skeletal_points(image_ocv)
        
        if head_point and foot_point:
            self._draw_points(image_ocv, head_point, foot_point)
            height = self._calculate_height(head_point, foot_point)
            if height:
                status_text = f"Height: {height:.2f} cm"
                color = (0, 255, 0)
            else:
                status_text = "No depth data"
                color = (0, 0, 255)
                height = None
        else:
            status_text = "No person detected"
            color = (0, 0, 255)
            height = None

        cv2.putText(image_ocv, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return height, image_ocv

    def _draw_points(self, image: np.ndarray, head_point: tuple, foot_point: tuple):
        for point, color in [(head_point, (255, 0, 0)), (foot_point, (0, 255, 255))]:
            bbox_start = (point[0] - 5, point[1] - 5)
            bbox_end = (point[0] + 5, point[1] + 5)
            cv2.rectangle(image, bbox_start, bbox_end, color, -1)

    def _calculate_height(self, head_point: tuple, foot_point: tuple) -> Optional[float]:
        try:
            err_h, head_depth = self.point_cloud.get_value(head_point[0], head_point[1])
            err_f, foot_depth = self.point_cloud.get_value(foot_point[0], foot_point[1])
            
            if err_h == sl.ERROR_CODE.SUCCESS and err_f == sl.ERROR_CODE.SUCCESS:
                base_height_in_meters = abs(head_depth[1] - foot_depth[1])
                height_in_meters = (base_height_in_meters * 0.1) * self.diff_rate + self.diff_const
                return int(height_in_meters)
            
        except Exception as e:
            print(f"Depth data error: {e}")
        
        return None

    def close(self):
        self.camera.close()

class HeightMeasurementHandler(socketserver.BaseRequestHandler):
    def handle(self):
        height_measurement = HeightMeasurement()
        
        if not height_measurement.open_camera():
            return
        
        print("Started streaming. Press Ctrl+C to stop.")
        
        try:
            while True:
                height, frame = height_measurement.process_frame()
                
                if frame.size > 0:
                    # Encode frame to JPEG
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                    _, jpeg_data = cv2.imencode('.jpeg', frame, encode_param)
                    data = jpeg_data.tobytes()
                    
                    # Send frame size followed by frame data
                    size = len(data).to_bytes(4, byteorder='big')
                    try:
                        self.request.sendall(size + data)
                    except Exception as e:
                        print(f"Connection error: {e}")
                        break
                    
                    if height is not None:
                        print(f"Current height: {height:.2f} cm")
                
        except Exception as e:
            print(f"Streaming error: {e}")
        finally:
            height_measurement.close()
            print("Stream ended")

def main():
    HOST = '172.25.15.27'
    PORT = 5700
    
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), HeightMeasurementHandler)
    
    print(f"Server starting on {HOST}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
        print("Server stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()