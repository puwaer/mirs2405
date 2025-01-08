import pyzed.sl as sl
import numpy as np
import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Function to get skeletal points
def get_skeletal_points(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        head_point = (int(landmarks[mp_pose.PoseLandmark.NOSE].x * image.shape[1]),
                      int(landmarks[mp_pose.PoseLandmark.NOSE].y * image.shape[0]))
        foot_point = (int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * image.shape[1]),
                      int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * image.shape[0]))
        return head_point, foot_point
    return None, None

def main():
    # Initialize ZED camera
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.ULTRA

    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(f"カメラのオープンに失敗: {status}")
        return

    # Get camera resolution - Updated for newer ZED SDK
    camera_info = cam.get_camera_information()
    width = camera_info.camera_configuration.resolution.width
    height = camera_info.camera_configuration.resolution.height

    # Prepare image containers
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()

    print("測定を開始します。'q'で終了します")

    while True:
        if cam.grab() == sl.ERROR_CODE.SUCCESS:
            # Retrieve image
            cam.retrieve_image(image, sl.VIEW.LEFT)
            cam.retrieve_measure(depth, sl.MEASURE.DEPTH)
            cam.retrieve_measure(point_cloud, sl.MEASURE.XYZ)

            # Convert to numpy array (this is the key fix)
            image_ocv = image.get_data()
            image_ocv = np.array(image_ocv, dtype=np.uint8)  # Ensure it's a numpy array with correct dtype

            # Check the shape and type of the image
            print(f"Image shape: {image_ocv.shape}, dtype: {image_ocv.dtype}")

            # Now convert RGBA to BGR
            try:
                image_ocv = cv2.cvtColor(image_ocv, cv2.COLOR_RGBA2BGR)
            except cv2.error as e:
                print(f"画像変換エラー: {e}")
                continue

            # Get skeletal points
            head_point, foot_point = get_skeletal_points(image_ocv)

            if head_point and foot_point:
                # 頭頂部と足元の位置を描画
                head_bbox_start = (head_point[0] - 5, head_point[1] - 5)
                head_bbox_end = (head_point[0] + 5, head_point[1] + 5)
                foot_bbox_start = (foot_point[0] - 5, foot_point[1] - 5)
                foot_bbox_end = (foot_point[0] + 5, foot_point[1] + 5)
                
                cv2.rectangle(image_ocv, head_bbox_start, head_bbox_end, (255, 0, 0), -1)  # 青色
                cv2.rectangle(image_ocv, foot_bbox_start, foot_bbox_end, (0, 255, 255), -1)  # 黄色

            # 深度画像処理

            # 深度データの取得
            try:
                err_h, head_depth = point_cloud.get_value(head_point[0], head_point[1])
                err_f, foot_depth = point_cloud.get_value(foot_point[0], foot_point[1])
                
                if err_h == sl.ERROR_CODE.SUCCESS and err_f == sl.ERROR_CODE.SUCCESS:
                    base_height_in_meters = abs(head_depth[1] - foot_depth[1])
                    diff_plus = 25
                    diff_rate = 1.18
                    #height_in_meters = (base_height_in_meters * 0.1) + diff_plus                       
                    height_in_meters = (base_height_in_meters * 0.1) * diff_rate                # Y座標の差分(diff), 倍率(diff_rate)
                    status_text = f"height: {height_in_meters:.2f} cm"
                    color = (0, 255, 0)  # 緑色
                    print(f"height: {height_in_meters:.2f} cm")
                else:
                    status_text = "有効な深度データが取得できません"
                    color = (0, 0, 255)  # 赤色
            except Exception as e:
                #print(f"深度データ取得エラー: {e}")
                status_text = "深度データ取得エラー"
                color = (0, 0, 255)  # 赤色

            # 状況テキストを描画
            cv2.putText(image_ocv, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # ウィンドウに画像を表示
            cv2.imshow("ZED Height Measurement", image_ocv)

            # 'q'キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cam.close()
    cv2.destroyAllWindows()
    print("終了しました")

if __name__ == "__main__":
    main()
