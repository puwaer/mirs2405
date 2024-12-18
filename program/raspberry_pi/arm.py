#ロボットアーム数値計算

import math
import numpy as np
import time
import config
from serial_mas_ras import init_serial, send_matrix, close_serial
from serial_sla_ras import


def arm():
    end_effecter = send_data_jr()    #シリアル通信（jetson to raspberrry pi）の関数呼び出し


    #数値計算
    x=l1*math.cos(theta1)+l2*math.cos(theta1+theta2)+
    y=l1*math.sin(theta1)+l2*math.sin(theta1+theta2)+

    # シリアル通信の初期化
    ser = init_serial()

    # 各間接角度
    joint_angle = np.array([[1, 2], [3, 4]])
    
    # 行列をピコに送信
    send_matrix(ser, joint_angle)

    # シリアルポートをクローズ
    close_serial(ser)

    if __name__ == "__main__":
        arm()