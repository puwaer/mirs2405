import numpy as np
import target_range, target_decide, theta_calcu, theta_clean

#import pdb
#from color import Color


"""
機体正面 -> x, 高さ -> y, 機体右 -> z
θの可動域は考えてません!
"""

# difine
L = [0.425, 0.426225, 0.1]                        # 各リンクの長さ

# ダミーデータ
x_target, y_target, z_target = 0.1, 0.5, 0.7      # 目標座標  
w = -1                                            # エンドエフェクタの向き: 1 -> 上向き, -1 -> 下向き

target_range.x_range_check(L, z_target, w)                      # zのt目標座標からxの取りうる範囲を決定、その時の角度計算
#x_target, z_target = target_decide.decide(P, y_target)         # 画像データから目標座標を決定
data = theta_calcu.calucuetion(L, x_target, z_target, w)        # θを計算する (アーム)

φ_0 = theta_calcu.horaizon(x_target, y_target)                  # θを計算する (ターンテーブル)
φ_1, φ_2 = theta_clean.theta_convers(data)                      # πから見た角度にする


#print(data)
print(f"φ_0 = {np.rad2deg(φ_0)}, φ_1 = {np.rad2deg(φ_1)}, φ_2 = {np.rad2deg(φ_2)} ")