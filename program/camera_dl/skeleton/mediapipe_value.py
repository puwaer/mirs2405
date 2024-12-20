import cv2
import mediapipe as mp
import numpy as np

class HeightEstimator:
    def __init__(self, initial_height=170):
        self.calibration_height = initial_height  # 初期値設定
        self.calibration_factor = None
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def estimate_height(self, landmarks):
        if not landmarks:
            return None, None
        
        # 必要なランドマークの取得
        shoulder_mid = landmarks[11]  # 右肩
        hip_mid = landmarks[23]      # 右腰
        ankle = landmarks[27]        # 右足首
        
        # 肩から足首までの距離を計算
        total_height_pixels = self.calculate_distance(shoulder_mid, ankle)
        
        # キャリブレーションファクターの計算または使用
        if self.calibration_factor is None:
            self.calibration_factor = self.calibration_height / total_height_pixels
        
        # 推定身長の計算 (cm)
        estimated_height = total_height_pixels * self.calibration_factor
        
        return estimated_height

    def adjust_height(self, adjustment):
        # キャリブレーション値の調整
        self.calibration_height += adjustment
        # キャリブレーションファクターをリセットして再計算を強制
        self.calibration_factor = None
        return self.calibration_height

def main():
    # 身長推定器の初期化
    estimator = HeightEstimator()
    
    # カメラのセットアップ
    cap = cv2.VideoCapture(1)
    
    print("\n=== 操作方法 ===")
    print("W: +1cm")
    print("S: -1cm")
    print("D: +5cm")
    print("A: -5cm")
    print("q: 終了\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # 画像の前処理
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = estimator.pose.process(frame_rgb)
        
        if results.pose_landmarks:
            # ランドマークの描画
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                estimator.mp_pose.POSE_CONNECTIONS
            )
            
            # 身長の推定
            landmarks = results.pose_landmarks.landmark
            estimated_height = estimator.estimate_height(landmarks)
            
            # 推定身長の表示
            if estimated_height is not None:
                height_text = f"Estimated Height: {estimated_height:.1f} cm"
                calibration_text = f"Calibration Height: {estimator.calibration_height:.1f} cm"
                
                # 推定身長を表示
                cv2.putText(
                    frame,
                    height_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # キャリブレーション値を表示
                cv2.putText(
                    frame,
                    calibration_text,
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 165, 0),
                    2
                )
        
        # 結果の表示
        cv2.imshow("Height Estimation", frame)
        
        # キー入力の処理
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):  # 終了
            break
        elif key == ord('w'):  # W キー
            estimator.adjust_height(1)
        elif key == ord('s'):  # S キー
            estimator.adjust_height(-1)
        elif key == ord('d'):  # D キー
            estimator.adjust_height(5)
        elif key == ord('a'):  # A キー
            estimator.adjust_height(-5)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()