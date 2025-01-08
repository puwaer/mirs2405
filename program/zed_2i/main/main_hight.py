import cv2
from zed_hight_class import HeightMeasurement


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