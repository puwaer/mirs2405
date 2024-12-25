import cv2
import mediapipe as mp
import numpy as np

# キャリブレーション設定
CALIBRATION_HEIGHT = 170  #ハイパラメータ,身長を設定(cm) カメラの特徴により変化

def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def estimate_height(landmarks, calibration_height, calibration_factor=None):
    if not landmarks:
        return None, None
    
    # 必要なランドマークの取得
    shoulder_mid = landmarks[11]  # 右肩
    hip_mid = landmarks[23]      # 右腰
    ankle = landmarks[27]        # 右足首
    
    # 肩から足首までの距離を計算
    total_height_pixels = calculate_distance(shoulder_mid, ankle)
    
    # キャリブレーションファクターの計算または使用
    if calibration_factor is None:
        calibration_factor = calibration_height / total_height_pixels
    
    # 推定身長の計算 (cm)
    estimated_height = total_height_pixels * calibration_factor
    
    return estimated_height, calibration_factor

def main():
    calibration_factor = None
    
    # カメラのセットアップ
    cap = cv2.VideoCapture(1)
    
    # MediaPipe Poseの初期化
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # 画像の前処理
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            # ランドマークの描画
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            
            # 身長の推定
            landmarks = results.pose_landmarks.landmark
            estimated_height, new_calibration_factor = estimate_height(
                landmarks,
                CALIBRATION_HEIGHT,
                calibration_factor
            )
            
            # 最初の有効な推定値でキャリブレーションを行う
            if calibration_factor is None and new_calibration_factor is not None:
                calibration_factor = new_calibration_factor
            
            # 推定身長の表示
            if estimated_height is not None:
                height_text = f"Estimated Height: {estimated_height:.1f} cm"
                cv2.putText(
                    frame,
                    height_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
        
        # 結果の表示
        cv2.imshow("Height Estimation", frame)
        
        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()