import pyzed.sl as sl
import numpy as np
import cv2
import math

def init_camera():
    # カメラの初期化
    zed = sl.Camera()
    
    # カメラパラメータの設定
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # 解像度設定
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # 深度モード設定
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP  # 座標系設定
    
    # カメラを開く
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"カメラの初期化に失敗しました: {err}")
        return None
    return zed

def measure_height():
    # カメラの初期化
    zed = init_camera()
    if zed is None:
        return
    
    # RuntimeParametersの設定
    runtime_params = sl.RuntimeParameters()
    runtime_params.confidence_threshold = 50
    
    try:
        while True:
            # 画像とデプス情報の取得用のオブジェクト作成
            image = sl.Mat()
            depth = sl.Mat()
            point_cloud = sl.Mat()
            
            # フレームの取得
            if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
                # 画像の取得
                zed.retrieve_image(image, sl.VIEW.LEFT)
                # 深度マップの取得
                zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
                # ポイントクラウドの取得
                zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
                
                # OpenCV形式に変換
                img_np = np.array(image.get_data())
                # NumPy配列の型を確認して変換
                if img_np.dtype != np.uint8:
                    img_np = img_np.astype(np.uint8)
                
                # 画像の表示（RGBAのままで表示）
                cv2.imshow("ZED", img_np)
                
                # キー入力の待機
                key = cv2.waitKey(1)
                
                # スペースキーが押されたら身長を測定
                if key == 32:  # スペースキー
                    # 画像の中心付近の深度情報を取得
                    height, width = img_np.shape[:2]
                    center_x = width // 2
                    center_y = height // 2
                    
                    # ポイントクラウドから3D座標を取得
                    point3D = point_cloud.get_value(center_x, center_y)
                    
                    # 床からの高さを計算（Y座標が高さに相当）
                    if not math.isnan(point3D[1]):
                        height_meters = abs(point3D[1])
                        print(f"測定された身長: {height_meters:.2f}m")
                    else:
                        print("深度情報を取得できませんでした。")
                
                # ESCキーで終了
                elif key == 27:
                    break
    
    finally:
        # リソースの解放
        zed.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    measure_height()

