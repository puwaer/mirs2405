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
from receive import receive_array_once
from receive import judge_angle
from receive import receive_distance
from send import send_angle

def main():
    while True: 
        jetson_data = receive_array_once('0.0.0.0', 12340)
        distance = receive_distance()
        if distance <= 2:
            jetson_data = receive_array_once('0.0.0.0', 12340)
            if mode == wait:
                if jetson_data[1] == 1:
                    mode=give

            else mode == give:
                jetson_data = receive_array_once('0.0.0.0', 12340)
                #serial_rc()
                data = judge_angle(jetson_data[0])
                send_angle(data)
                pr_state = receive_pr()
                if pr_state[1] == 1:
                    mode = refill

            else mode == refill
                pr_state = receive_pr()
                if pr_state == 0:
                    data = [3, 0, 0, 0, 0, 0 ,0]    #配布物を取得
                    send_angle(data)
                mode = wait
        else:
            #send_run()

#実行
mode =wait
main()

