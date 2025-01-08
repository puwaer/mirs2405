import pyzed.sl as sl
import numpy as np

def main():
    # ZEDカメラの初期化
    cam = sl.Camera()
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # 高精度の深度モード
    init_params.coordinate_units = sl.UNIT.METER  # 深度の単位をメートルに設定
    
    if cam.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("カメラの初期化に失敗しました")
        return
    
    runtime_params = sl.RuntimeParameters()
    depth_image = sl.Mat()
    
    print("測定を開始します。'q'で終了します")
    while True:
        if cam.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
            # 深度画像の取得
            cam.retrieve_measure(depth_image, sl.MEASURE.DEPTH)
            
            # 画像サイズの取得
            width = depth_image.get_width()
            height = depth_image.get_height()
            
            # 頭頂部と足元の座標を仮定（中央縦線上の上部と下部）
            head_point = [width // 2, height // 4]
            foot_point = [width // 2, 3 * height // 4]
            
            # 深度データの取得
            head_depth = depth_image.get_value(*head_point)[1]
            foot_depth = depth_image.get_value(*foot_point)[1]
            
            if head_depth > 0 and foot_depth > 0:  # 有効な深度値がある場合
                height_in_meters = abs(head_depth - foot_depth)
                print(f"推定身長: {height_in_meters:.2f} m")
            else:
                print("有効な深度データが取得できませんでした")
        
        # 終了チェック
        if input("続行するにはEnterキーを押してください（終了するには'q'を入力）: ") == 'q':
            break
    
    cam.close()
    print("終了しました")

if __name__ == "__main__":
    main()
