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
from receive import receive_distance
from receive import judge_angle
from send import send_angle

def main():
    while True: 

        distance = receive_distance()
        camera_data = receive_camera()
        arm_angle = judge_angle(camera_data[0])
        joint1_angle = arm_angle[0]
        data = [3, arm_angle[0], arm_angle[1], arm_angle[2], arm_angle[3], 0, 0]
        send_angle(data)    
            while True:
                distance = receive_distance()
                if 20 < distance <= 35:
                    joint1_angle -= 1
                    
                elif 35 < distance < 45:
                    break
                elif 45 < distance < 150:
                    joint1_angle += 1
                else:
                    break
                if joint1_angle < -65:
                    joint1_angle = -65
                elif joint1_angle > 65:
                    joint1_angle = 65
                    
                data = [3,joint1_angle, arm_angle[1], arm_angle[2], arm_angle[3], 0, 0]
                send_angle(data)   
                time.sleep(0.1)
                
            #position = [camera_data[3], camera_data[4]]
            #serial_rc()
            
            pr_state = receive_pr()
            if pr_state[1] == 1:
                mode='refill'

        elif mode=='refill':
            pr_state = receive_pr()
            if pr_state == 0:
                data = [3, 0, 0, 0, 0, 0 ,0]    #配布物を取得
                send_angle(data)
            mode = 'wait'
        else:
            send_run()

#実行
mode = 'wait'
main()
