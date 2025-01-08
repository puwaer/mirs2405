import config  # 設定ファイルをインポート
import time
import sys
sys.path.append("./angle_decide")
from receive import receive_pr
from receive import serial_rc  # シリアル通信関数をインポート
from receive import judge_angle
from receive import receive_distance
from receive import receive_array_once
from send import send_angle
from inverse_kinematics import inverse_kinematics


#身長から角度決定
received_array = receive_array_once('0.0.0.0', 12340)
print(received_array[0])
#hight = receive_camera
#hight = [139, 0, 0, 0, 0]
angle = judge_angle(received_array[0])
print(angle)
send_angle(angle)

'''
#角度計算
def test_arm():
    L = [0.425, 0.426225, 0.1]
    x_target = 0.3
    y_target = 0.5
    z_target = 0.4
    w = 1    
    angle = inverse_kinematics(L, x_target, y_target, z_target, w)
    #print(a)
    print(a[2])
test_arm()
'''

'''
#rc操作
def test_rc():
    serial_rc()
test_rc()
'''

'''
#角度送信
def test_angle():
    data = [3, 10, -10, 0, 0, 0, 0]
    send_angle(data)
test_angle()
'''
'''
#フォトリフレクタ値の受信
def test_pr():
    print("Starting receive_pr...")
    pr_state = receive_pr()  # receive.pyの関数を呼び出す

    # データを確認
    if pr_state:
        print("Received data:", pr_state[1])
    else:
        print("No data received.")
'''
'''
#超音波から距離を取得
def test_distance():
    distance = receive_distance()
    print(distance[1])
'''
'''
#test_pr()
#time.sleep(2)
while True:
    test_distance()
'''
'''
#raspi側シリアル通信
def test_jetson():
    received_array = receive_array(port="/dev/ttyS0", baudrate=115200)
    print(received_array)
test_jetson()

#jetson側シリアル通信
def test_raspi():
    while True:
        array_to_send = [170, 0]
        send_array(port="/dev/ttyUSB0", baudrate=115200, array=array_to_send)
test_raspi()
'''

