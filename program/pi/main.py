#raspberry pi 全体動作メインプログラム
import math
import numpy as np
import time
import sys
sys.path.append("./angle_decide")
import config
from inverse_kinematics import inverse_kinematics
from receive import receive_pr
from receive import serial_rc
from send import send_angle

def main():
    while True: 
        lidar_data = receive_lidar()
        if lidar_data <= 2:
            camera_data = receive_camera()  #カメラデータの受取
            if mode=wait:
                if camera_data[0] ==1 and camera_data[1] == 1 and camera_data[2] == 1:  #人の認識、年齢、性別が条件適合
                    mode=give

            else mode=give:
                camera_data = receive_camera()
                #position = [camera_data[3], camera_data[4]]
                #serial_rc()
                L = [0.425, 0.426225, 0.1]
                x_target = camera_data[3]
                y_target = camera_data[4]
                z_target = camera_data[5]
                w = 1   
                arm_angle = inverse_kinematics(L, x_target, y_target, z_target, w)
                data = [3, arm_angle[0], arm_angle[1], arm_angle[2], arm_angle[3], 0, 0]
                send_angle(data)
                pr_state = receive_pr()
                if pr_state[1] == 1:
                    mode=refill

            else mode=refill
                pr_state = receive_pr()
                if pr_state == 0:
                    w = -1
                    data = [3, 0, 0, 0, 0, 0 ,0]    #配布物を取得
                    send_angle(data)
                mode = wait
        else:
            send_run()

#実行
mode =wait
#w = 1
main()

