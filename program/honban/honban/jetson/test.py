#import config  # 設定ファイルをインポート
import time
from send import send_array


#jetson側シリアル通信
def test_raspi():
    while True:
        array_to_send = [170, 0]
        send_array(port="/dev/ttyUSB0", baudrate=115200, array=array_to_send)
test_raspi()


