#ロボットアーム数値計算

import math
import numpy as np
import time

serial()    #jetsonからエンドエフェクタ取得

L = [1,1,1,1,1]     #関節長さ
start_theta = [0,0,0,0,0]
current_theta = []
goal_theta = []
end_effecter = [x,y,z]
lambda = np.array[1,1,1]

qx = lambda[1]*math.sin(theta)
qy = lambda[2]*math.sin(theta)
qz = lambda[3]*math.sin(theta)
qw = math.cos(theta)
quaternion  = [qx,qy,qz,qw]

position_4 = end_effecter-(L[4]+L[5])*




#数値計算



x=l1*math.cos(theta1)+l2*math.cos(theta1+theta2)+
y=l1*math.sin(theta1)+l2*math.sin(theta1+theta2)+






