import cv2
import pyzed.sl as sl
import mediapipe as mp

# ZEDカメラの設定
zed = sl.Camera()
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080  # 解像度を設定
init_params.camera_fps = 30  # FPSを設定
status = zed.open(init_params)

if status != sl.ERROR_CODE.SUCCESS:
    print("ZEDカメラの初期化に失敗しました")
    exit()

# MediaPipeのセットアップ
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# ZEDの画像フレームを準備
image = sl.Mat()

# 骨格推定用のMediaPipe Poseモデルを初期化
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        # ZEDから画像を取得
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # 画像をMat形式からOpenCV形式に変換
            zed.retrieve_image(image, sl.VIEW.LEFT)  # 左目の画像を取得
            frame = image.get_data()

            # BGRに変換
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

            # 骨格推定を実行
            results = pose.process(frame_rgb)

            # 骨格を描画
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 画像を表示
            cv2.imshow("ZED Pose Estimation", frame_rgb)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 後片付け
zed.close()
cv2.destroyAllWindows()
