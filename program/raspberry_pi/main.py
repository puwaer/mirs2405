#raspberry pi 全体動作プログラム
import math
import numpy as np
import time
import arm
import config
import serial

def main():
serial()        #jetsonから座標を受信

arm()           #ロボットアーム間接角度計算

serial()        #arduino,picoに座標、アーム間接角度を送信

serial()        #picoから受け取り完了を受信

serial()        #arduino,picoに受け取り完了を送信

if __name__ == "__main__":
    main()
