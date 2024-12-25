import numpy as np
#import pdb

import theta_choice, theta_clean
from color import Color


# 入力の目標座標から角度θを計算する   
def calucuetion(L, x_target, z_target, w):
    if not abs(w) == 1:
        #print("ERROR!")
        return()

    # 第2関節の座標を計算
    x_2 = x_target - L[2] * np.cos(w * np.pi / 2)
    z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

    u = x_2**2 + z_2**2
    l = np.sqrt(u)

    # 到達可能か？
    if L[0] + L[1] < l:
        #print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")
        data = ([False, "None", "None", "None", "None"])
        return(data)


    # θ_2の候補の計算
    cosθ_2 = (u - L[0]**2 - L[1]**2 ) / (2 * L[0] * L[1] )

    if not -1 <= cosθ_2 <= 1:
        # print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")
        data = ([False, "None", "None", "None", "None"])
        return(data)

    θ_2_1 = np.arccos(cosθ_2)
    θ_2_2 = -θ_2_1
    θ_2_3 = θ_2_1 + np.pi/2
    θ_2_4 = θ_2_2 + np.pi/2
    θ_2_5 = θ_2_3 + np.pi/2
    θ_2_6 = θ_2_4 + np.pi/2
    θ_2_7 = θ_2_5 + np.pi/2
    θ_2_8 = θ_2_6 + np.pi/2

    θ_2_kouho = [θ_2_1, θ_2_2, θ_2_3, θ_2_4, θ_2_5, θ_2_6, θ_2_7, θ_2_8]


    # θ_1の候補の計算
    φ_2 = np.arctan2(x_2, z_2 )
    cosθ_1u = (u + L[0]**2 - L[1]**2) / (2 * L[0] * l)

    if not -1 <= cosθ_1u <= 1:
        #print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")
        data = ([False, "None", "None", "None", "None"])
        return(data)

    θ_1u = np.arccos(cosθ_1u)

    θ_1_1 = φ_2 + θ_1u
    θ_1_2 = θ_1_1 + np.pi/2
    θ_1_3 = θ_1_1 + np.pi
    θ_1_4 = θ_1_1 - np.pi/2 

    θ_1_5 = -θ_1_1
    θ_1_6 = -θ_1_5 + np.pi/2
    θ_1_7 = -θ_1_5 + np.pi
    θ_1_8 = -θ_1_5 - np.pi/2
    
    θ_1_9 = φ_2 - θ_1u
    θ_1_10 = θ_1_9 + np.pi/2
    θ_1_11 = θ_1_9 + np.pi
    θ_1_12 = θ_1_9 - np.pi/2

    θ_1_13 = -θ_1_9
    θ_1_14 = θ_1_13 + np.pi/2
    θ_1_15 = θ_1_13 + np.pi
    θ_1_16 = θ_1_13 - np.pi/2

    θ_1_kouho = [θ_1_1, θ_1_2, θ_1_3, θ_1_4, θ_1_5, θ_1_6, θ_1_7, θ_1_8, θ_1_9, θ_1_10, θ_1_11, θ_1_12, θ_1_13, θ_1_14, θ_1_15, θ_1_16]


    # 角度の正規化 (-πからπにする)
    θ_1, θ_2, θ_3 = theta_clean.normalization2(θ_1_kouho, θ_2_kouho, None)


    # θ_1, θ_2の候補から最適な組を選ぶ
    θ_1, θ_2 = theta_choice.choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w)

    if θ_1 == None or θ_2 == None:
        # print(f"目標 ({x_target:.2f}, {z_target:.2f}) は到達不可能です。")
        data = ([False, "None", "None", "None", "None"])
        return(data)


    # θ_1, θ_2からθ_3を決定
    θ_3 = w * np.pi/2 - θ_1 - θ_2


    # 角度の正規化 (-πからπにする)
    θ_1, θ_2, θ_3 = theta_clean.normalization1(θ_1, θ_2, θ_3)


    # 順運動学で座標を逆算する
    x_reverse = L[0] * np.cos(θ_1) + L[1] * np.cos(θ_1 + θ_2) + L[2] * np.cos(θ_1 + θ_2 + θ_3)
    z_reverse = L[0] * np.sin(θ_1) + L[1] * np.sin(θ_1 + θ_2) + L[2] * np.sin(θ_1 + θ_2 + θ_3)


    # 目標値との誤差
    error_x = x_target - x_reverse
    error_z = z_target - z_reverse
    error = np.sqrt(error_x**2 + error_z**2)


    data = ([True, θ_1, θ_2, θ_3, error])
    #print(Color.GREEN, f"目標 ({x_target:.1f}, {z_target:.1f}): θ_1 = {np.rad2deg(θ_1):.2f}, θ_2 = {np.rad2deg(θ_2):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}", Color.RESET, sep = '')

    return(data)


# ターンテーブル(水平軸)の角度計算
def horaizon(x_target, y_target):
    φ_0 = np.arctan2(-y_target, x_target)       # 水平左側がプラス

    return(φ_0)