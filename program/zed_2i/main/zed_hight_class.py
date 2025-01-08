import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp
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
        self.diff_rate = 1.2  # 倍率
        
    def open_camera(self) -> bool:
        """カメラを開く"""
        status = self.camera.open(self.init_params)
        if status != sl.ERROR_CODE.SUCCESS:
            print(f"カメラのオープンに失敗: {status}")
            return False
        return True
        
    def get_skeletal_points(self, image: np.ndarray) -> Tuple[Optional[tuple], Optional[tuple]]:
        """骨格ポイントを取得"""
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
        """フレームを処理して身長を計算"""
        if self.camera.grab() != sl.ERROR_CODE.SUCCESS:
            return None, np.array([])

        # 画像とデプスデータの取得
        self.camera.retrieve_image(self.image, sl.VIEW.LEFT)
        self.camera.retrieve_measure(self.depth, sl.MEASURE.DEPTH)
        self.camera.retrieve_measure(self.point_cloud, sl.MEASURE.XYZ)

        # numpy配列に変換
        image_ocv = self.image.get_data()
        image_ocv = np.array(image_ocv, dtype=np.uint8)
        
        try:
            image_ocv = cv2.cvtColor(image_ocv, cv2.COLOR_RGBA2BGR)
        except cv2.error as e:
            print(f"画像変換エラー: {e}")
            return None, image_ocv

        # 骨格ポイントの取得
        head_point, foot_point = self.get_skeletal_points(image_ocv)
        
        if head_point and foot_point:
            # 骨格ポイントの描画
            self._draw_points(image_ocv, head_point, foot_point)
            
            # 深度データから身長を計算
            height = self._calculate_height(head_point, foot_point)
            if height:
                status_text = f"height: {height:.2f} cm"
                color = (0, 255, 0)  # 緑色
            else:
                status_text = "有効な深度データが取得できません"
                color = (0, 0, 255)  # 赤色
                height = None
        else:
            status_text = "骨格検出失敗"
            color = (0, 0, 255)  # 赤色
            height = None

        # ステータステキストの描画
        cv2.putText(image_ocv, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return height, image_ocv

    def _draw_points(self, image: np.ndarray, head_point: tuple, foot_point: tuple):
        """検出ポイントを描画"""
        for point, color in [(head_point, (255, 0, 0)), (foot_point, (0, 255, 255))]:
            bbox_start = (point[0] - 5, point[1] - 5)
            bbox_end = (point[0] + 5, point[1] + 5)
            cv2.rectangle(image, bbox_start, bbox_end, color, -1)

    def _calculate_height(self, head_point: tuple, foot_point: tuple) -> Optional[float]:
        """身長を計算"""
        try:
            err_h, head_depth = self.point_cloud.get_value(head_point[0], head_point[1])
            err_f, foot_depth = self.point_cloud.get_value(foot_point[0], foot_point[1])
            
            if err_h == sl.ERROR_CODE.SUCCESS and err_f == sl.ERROR_CODE.SUCCESS:
                base_height_in_meters = abs(head_depth[1] - foot_depth[1])
                height_in_meters = (base_height_in_meters * 0.1) * self.diff_rate
                return height_in_meters
            
        except Exception as e:
            print(f"深度データ取得エラー: {e}")
        
        return None

    def close(self):
        """カメラをクローズ"""
        self.camera.close()
        cv2.destroyAllWindows()

def main():
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
    main()