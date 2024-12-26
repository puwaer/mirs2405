import numpy as np

import theta_calcu

#import pdb
#from color import Color


def x_range_check(L, z_target, w):
    z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

    if L[0] + L[1] < z_2**2:
        #print(f"この高さ {z_target} には到達不可能です。")
        return

    x_target_MAX = np.sqrt((L[0] + L[1])**2 - z_2**2)
    x_target_min = -x_target_MAX

    #print(f"data1: x_target = {x_target_MAX}, z_target = {z_target}")
    data1 = theta_calcu.calucuetion(L, x_target_MAX, z_target, w)
    #print(f"data2: x_target = {0}, z_target = {z_target}")
    data2 = theta_calcu.calucuetion(L, 0, z_target, w)
    #print(f"data3: x_target = {x_target_min}, z_target = {z_target}")
    data3 = theta_calcu.calucuetion(L, x_target_min, z_target, w)

    return
