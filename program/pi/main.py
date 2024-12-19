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
    
    init()

def main():
    while True:
        if mode=wait:
            start_recognition()
            target_state = receive_target()
            if target_state[1] == 1
                mode=give

        else mode=give:
            receive_position()
            send_rc()
            arm()
            send_angle()
            if input_value[1] == 1:
                mode=refile

        else mode=refill
            send_init()
            possession_state = receive_possession()
            if possession_state_state == 0:
                get_handout()
            mode = wait

    if __name__ == "__main__":
    main()
