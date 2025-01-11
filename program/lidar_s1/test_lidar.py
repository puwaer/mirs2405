from rplidar import RPLidar

# シリアルポートとボーレートの設定
PORT_NAME = 'COM7'              # Windowsの場合の例
#PORT_NAME = '/dev/ttyUSB0'      # Linuxの場合

BAUDRATE = 115200   # または 256000
#pip install rplidar


def main():
    # RPLidarオブジェクトを初期化
    lidar = RPLidar(PORT_NAME, baudrate=BAUDRATE)
    
    try:
        print("RPLIDAR スキャンを開始します...")
        lidar.start_motor()  # モーターを起動

        # スキャンデータの取得
        for i, scan in enumerate(lidar.iter_scans()):
            print(f"スキャンデータ {i+1}:")
            
            # スキャンデータを表示
            for (_, angle, distance) in scan:
                print(f"角度: {angle:.2f}°, 距離: {distance:.2f} mm")
            
            # テストとして3回スキャンしたら終了
            if i == 2:
                break
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        print("RPLIDARを停止しています...")
        lidar.stop()         # スキャンを停止
        lidar.disconnect()   # デバイスから切断

if __name__ == '__main__':
    main()
