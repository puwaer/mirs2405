#raspberry pi 全体動作プログラム
import math
import numpy as np
import time
import sys
import arm
import config
import send
import receive


def init():
    mode=wait
    if devaice_recognition()==1
        mode=wait
    
    else
        sys.exit()
    

def main():
    while True:
        camera_data = receive_camera()
        if mode=wait:
            if camera_data[0] ==1 and camera_data[1] == 1 and camera_data[2] == 1:
                mode=give

        else mode=give:
            position = [camera_data[3], camera_data[4]]
            send_rc()
            arm()
            send_angle()
            ft_state = receive_ft()
            if ft_state[1] == 1:
                mode=refile

        else mode=refill
            remove_position()
            ft_state = receive_ft()
            if ft_state == 0:
                get_handout()
            mode = wait

init()
main()

