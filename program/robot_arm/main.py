#raspberry pi 全体動作プログラム
import math
import numpy as np
import time
import arm
import config
import serial


serial()        #jetsonから座標を受信

arm()           #ロボットアーム間接角度計算

serial()        #arduino,picoに座標、アーム間接角度を送信


