#raspberry pi 全体動作メインプログラム
import math
import numpy as np
import time
import serial
import sys
sys.path.append("./../zed")
import config
from read_json import read_json_name
#from inverse_kinematics import inverse_kinematics
from client_value_updata import get_camera
from receive import receive_pr
from receive import serial_rc
from receive import receive_distance
from receive import judge_angle
from send import send_angle
from send import get
'''
a = read_json_name(2)
print(a)
'''

def main_boos():
    ser_esp = serial.Serial(config.ESP_PORT, config.BAUDRATE)
    ser_pico = serial.Serial(config.PICO_PORT, config.BAUDRATE)
    ser_arduino = serial.Serial(config.ARDUINO_PORT, config.BAUDRATE)
    time.sleep(2)

    camera_data = []
    camera_data[0] = read_json_name(2)  #カメラデータの受取
    camera_data[1] = 1
    
    while True: 
    	serial_rc(ser_esp, ser_pico)
        if mode=='wait':
            if camera_data[1] == 1:
                mode='give'

        elif mode=='give':
            distance = receive_distance()
            camera_data[0] = read_json_name(2)  #カメラデータの受取
            camera_data[1] = 1
            arm_angle = judge_angle(camera_data[0])
            #joint1_angle = arm_angle[0]
            #data = [3, arm_angle[0], arm_angle[1], arm_angle[2], arm_angle[3], 0, 0]
            send_angle(arm_angle, ser_pico)
            
            while True:
                distance = receive_distance(ser_arduino)
                if 20 < distance <= 35:
                    arm_angle[1] += 1
                    
                elif 35 < distance < 45:
                    break
                elif 45 < distance < 150:
                    arm_angle[1] -= 1
                else:
                    break
                if arm_angle[1] < -70:
                    arm_angle[1] = -70
                elif arm_angle[1] > 70:
                    arm_angle[1] = 70
                    
                send_angle(arm_angle, ser_pico)   
                time.sleep(0.1)
                            
            pr_state = receive_pr(ser_pico)
            if pr_state[1] == 1:
                mode='refill'

        elif mode=='refill':
            pr_state = receive_pr(ser_pico)
            if pr_state == 0:
                get(ser_pico)
            mode = 'wait'
        #else:
            #send_run()
            

#実行
mode = 'refill'
main_boos()

