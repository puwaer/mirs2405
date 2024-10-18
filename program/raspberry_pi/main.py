#raspberry pi 全体動作プログラム
import math
import numpy as np
import time
import arm
import config
import serial_pi

def main():
    ser_jetson_to_pi = serial_pi.init_serial(config.port_jetson_to_pi)          #シリアル通信初期化
    position = serial_pi.receive_position(ser_jetson_to_pi)                     #jetsonから座標を受信
    print(f"Received position: {position}")                                     #座標表示

    arm()                                                                       #ロボットアーム間接角度計算

    ser_pi_to_pico = serial_pi.init_serial(config.port_pi_to_pico)
    position_angles = np.array([1, 2, 1, 1], dtype=np.float32)
    serial_pi.send_position_angles(ser_pi_to_pico, position_angles)

    ser_pi_to_arduino = serial_pi.init_serial(config.port_pi_to_arduino)
    angles = np.array([2, 2, 1], dtype=np.float24)
    serial_pi.send_angles(ser_pi_to_arduino, angles)

    serial_pi.close_serial(ser_jetson_to_pi)                                    #通信終了
    serial_pi.close_serial(ser_pi_to_pico)                                      #通信終了
    serial_pi.close_serial(ser_pi_to_arduino)                                   #通信終了

if __name__ == "__main__":
    main()
