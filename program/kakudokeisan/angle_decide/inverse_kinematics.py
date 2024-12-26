import numpy as np
import target_range, target_decide, theta_calcu, theta_clean

#import pdb
#from color import Color


"""
機体正面 -> x, 高さ -> y, 機体右 -> z (座標系の取り方が他のシステムと一致していない可能性があります！)
θの可動域は考えてません！
"""

# init
L = [0.425, 0.426225, 0.1]                        # 各リンクの長さ

# 仮データ (これは統合し次第消す)
x_target, y_target, z_target = 0.3, 0.5, 0.4      # 目標座標  
w = 1                                             # エンドエフェクタの向き: 1 -> 上向き(渡す時), -1 -> 下向き(掴む時)


def inverse_kinematics(L, x_target, y_target, z_target, w):
    #target_range.x_range_check(L, z_target, w)                     # zのt目標座標からxの取りうる範囲を決定、その時の角度計算
    #x_target, z_target = target_decide.decide(P, y_target)         # 画像データから目標座標を決定
    data = theta_calcu.calucuetion(L, x_target, z_target, w)        # θを計算する (アーム)

    φ_0 = theta_calcu.horaizon(x_target, y_target)                  # θを計算する (ターンテーブル)
    φ_1, φ_2, φ_3 = theta_clean.theta_convers(data)                 # π/2から見た角度にする (前側が正)

    φ = [φ_0, φ_1, φ_2, φ_3]

    #print(data)
    #print(f"φ_0 = {(np.rad2deg(φ_0)):.2f}, φ_1 = {(np.rad2deg(φ_1)):.2f}, φ_2 = {(np.rad2deg(φ_2)):.2f}, φ_3 = {(np.rad2deg(φ_3)):.2f}")

    return(φ)

φ = inverse_kinematics(L, x_target, y_target, z_target, w)