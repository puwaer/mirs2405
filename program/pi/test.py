#import math
#import numpy as np
import time
import serial
#import sys
#import arm
#import config
#from send import send_angle

from receive import receive_ft # 受信関数をインポート

def main():
    received_values = receive_ft()  # データを受信

    # 受信したデータを表示
    if received_values:
        print("Received data:", received_values)
        print(received_values[1])
        if received_values[1]==1:
            print("complete")
    else:
        print("No data received.")

if __name__ == "__main__":
    main()
