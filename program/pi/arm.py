#ロボットアーム数値計算

import math
import numpy as np
import time
import config
import serial_pi

def arm():
    end_effecter = serial_pi.receive_position()    #シリアル通信（jetson to raspberrry pi）の関数呼び出し
    theta = [0]*3
    L = [0.5, 0.5, 0.05]

    #数値計算
    x1=L[0]*math.cos(theta[0])
    x2=x1+L[1]*math.cos(theta[0]+theta[1])
    x3=x2+L[2]*math.cos(theta[0]+theta[1]+theta[2])

    y1=L[0]*math.sin(theta[1])
    y2=y1+L[1]*math.sin(theta[0]+theta[1])
    y3=y2+L[2]*math.sin(theta[0]+theta[1]+theta[2])    

    theta[0]=1
    theta[1]=1
    theta[2]=1


    if __name__ == "__main__":
        arm()