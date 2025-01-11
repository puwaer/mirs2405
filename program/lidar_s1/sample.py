from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
# 正しいポートを指定していることを確認
lidar.connect(port="COM7", baudrate=115200, timeout=3)
# 接続後、少し待機を入れる
time.sleep(2)