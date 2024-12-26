#from receive import receive_pr
import config  # 設定ファイルをインポート
from receive import serial_rc  # シリアル通信関数をインポート
from send import send_angle
import sys
sys.path.append("./angle_decide")
from inverse_kinematics import inverse_kinematics


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

test_pr()
'''