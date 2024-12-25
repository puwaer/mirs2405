import numpy as np
from datetime import datetime
import pdb

import thetachoice, clean, color
from color import Color


# 入力の目標座標から角度θを計算する   
def keisan1(L, x_target, z_target, w):
    if not abs(w) == 1:
        print("ERROR!")
        return()

    data = []

    x_2 = x_target - L[2] * np.cos(w * np.pi / 2)
    z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

    print("1: ", f"w = {w}, x_2 = {x_2}, z_2 = {z_2}")

    u = x_2**2 + z_2**2
    l = np.sqrt(u)

    # 到達可能か？
    if L[0] + L[1] < l:
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)


    # θ_2の候補の計算
    cosθ_2 = (u - L[0]**2 - L[1]**2 ) / (2 * L[0] * L[1] )

    if not -1 <= cosθ_2 <= 1:
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    θ_2_1 = np.arccos(cosθ_2) #+np.pi/16
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
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
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

    # θ_1, θ_2の候補から最適な組を選ぶ
    θ_1, θ_2 = thetachoice.choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w)

    if θ_1 == None or θ_2 == None:
        print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    # θ_1, θ_2からθ_3を決定
    θ_3 = w * np.pi/2 - θ_1 - θ_2

    # 角度の正規化 (-πからπにする)
    θ_1, θ_2, θ_3 = clean.normalization1(θ_1, θ_2, θ_3)

    # 順運動学で座標を逆算する
    x_reverse = L[0] * np.cos(θ_1) + L[1] * np.cos(θ_1 + θ_2) + L[2] * np.cos(θ_1 + θ_2 + θ_3)
    z_reverse = L[0] * np.sin(θ_1) + L[1] * np.sin(θ_1 + θ_2) + L[2] * np.sin(θ_1 + θ_2 + θ_3)

    # 目標値との誤差
    error_x = x_target - x_reverse
    error_z = z_target - z_reverse
    error = np.sqrt(error_x**2 + error_z**2)

    # データをリストに追加
    data_i = [L[0], L[1], L[2], x_target, z_target, True, θ_1, θ_2, θ_3, error]
    data.append (data_i)

    #print(f"x_3 = {x_reverse}, z_3 = {z_reverse}")
    #print(f"θ_1 = {θ_1}, θ_2 = {θ_2}, θ_3 = {θ_3}")
    print(Color.GREEN, f"目標 ({x_target:.1f}, {z_target:.1f}): θ_1 = {np.rad2deg(θ_1):.2f}, θ_2 = {np.rad2deg(θ_2):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}", Color.RESET, sep = '')
    return(data)

# 候補を絞らず全て採択する
def keisan2(L, x_target, z_target, w):
    data = []

    x_2 = x_target - L[2] * np.cos(w * np.pi / 2)
    z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

    # 到達可能か？
    u = x_2**2 + z_2**2
    l = np.sqrt(u)

    if L[0] + L[1] < l:
        print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    cosθ_2 = (u - L[0]**2 - L[1]**2 ) / (2 * L[0] * L[1] )
    if not -1 <= cosθ_2 <= 1:
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    θ_2_1 = np.arccos(cosθ_2) #+ np.pi/8
    θ_2_2 = -θ_2_1
    θ_2_3 = np.pi - θ_2_1
    θ_2_4 = -θ_2_3
    θ_2_5 = θ_2_1 + np.pi/2
    θ_2_6 = θ_2_2 + np.pi/2
    θ_2_7 = θ_2_3 + np.pi/2
    θ_2_8 = θ_2_4 + np.pi/2

    θ_2_kouho = [θ_2_1, θ_2_2, θ_2_3, θ_2_4, θ_2_5, θ_2_6, θ_2_7, θ_2_8]

    φ_2 = np.arctan2(x_2, z_2 )
    cosθ_1u = (u + L[0]**2 - L[1]**2) / (2 * L[0] * l)

    if not -1 <= cosθ_1u <= 1:
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
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

    θ_1, θ_2 = thetachoice.choicetheta2(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w)

    print (f"θ_1_1 = {θ_1_1}")
    print (f"θ_1_2 = {θ_1_2}")
    print (f"θ_1_3 = {θ_1_3}")
    print (f"θ_1_4 = {θ_1_4}")
    print (f"θ_1_5 = {θ_1_5}")
    print (f"θ_1_6 = {θ_1_6}")
    print (f"θ_1_7 = {θ_1_7}")
    print (f"θ_1_8 = {θ_1_8}")
    print (f"θ_2_1 = {θ_2_1}")
    print (f"θ_2_2 = {θ_2_2}")
    print (f"θ_2_3 = {θ_2_3}")
    print (f"θ_2_4 = {θ_2_4}")
    print (f"θ_2_5 = {θ_2_5}")
    print (f"θ_2_6 = {θ_2_6}")
    print (f"θ_2_7 = {θ_2_7}")
    print (f"θ_2_8 = {θ_2_8}")

    if θ_1 == None or θ_2 == None:
        print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    for i in range(len(θ_1)):

        θ_3 = w * np.pi/2 - θ_1[i] - θ_2[i]

        # 角度の正規化
        θ_1[i], θ_2[i], θ_3 = clean.normalization1(θ_1[i], θ_2[i], θ_3)

        x_reverse = L[0] * np.cos(θ_1[i]) + L[1] * np.cos(θ_1[i] + θ_2[i]) + L[2] * np.cos(θ_1[i] + θ_2[i] + θ_3)
        z_reverse = L[0] * np.sin(θ_1[i]) + L[1] * np.sin(θ_1[i] + θ_2[i]) + L[2] * np.sin(θ_1[i] + θ_2[i] + θ_3)

        # 目標値との誤差
        error_x = x_target - x_reverse
        error_z = z_target - z_reverse
        error = np.sqrt(error_x**2 + error_z**2)
    
        print(Color.GREEN, f"目標 ({x_target:.1f}, {z_target:1f}): θ_1 = {np.rad2deg(θ_1[i]):.2f}, θ_2 = {np.rad2deg(θ_2[i]):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}", Color.RESET, sep = '')
        print(Color.GREEN, f"到達 ({x_reverse:.3f}, {z_reverse:.3f})", Color.RESET, sep = '')

        # データをリストに追加
        data_i = [L[0], L[1], L[2], x_target, z_target, True, θ_1[i], θ_2[i], θ_3, error]
        data.append (data_i)

    return(data)


# なにこれ
def keisan3(L, x_target, z_target, w):
    data = []

    x_2 = x_target - L[2] * np.cos(w * np.pi / 2)
    z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

    # 到達可能か？
    u = x_2**2 + z_2**2
    l = np.sqrt(u)

    if L[0] + L[1] < l:
        print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    cosθ_2 = (u - L[0]**2 - L[1]**2 ) / (2 * L[0] * L[1] )
    if not -1 <= cosθ_2 <= 1:
        print(f"目標 ({x_target:.1f}, {z_target:.1f}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    θ_1_kouho = np.linspace(-np.pi, np.pi, 500)  # 角度範囲が広がっているか
    θ_2_kouho = np.linspace(-np.pi, np.pi, 500)

    θ_1, θ_2 = thetachoice.choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w)

    #print (f"θ_1_kouho = {θ_1}, θ_2_kouho = {θ_2}")

    if θ_1 == None or θ_2 == None:
        print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

        # データをリストに追加
        data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
        return(data)

    """
    for i in range(len(θ_1)):

        θ_3 = w * np.pi/2 - θ_1[i] - θ_2[i]

        # 角度の正規化
        θ_1[i], θ_2[i], θ_3 = clean.normalization1(θ_1[i], θ_2[i], θ_3)

        x_reverse = L[0] * np.cos(θ_1[i]) + L[1] * np.cos(θ_1[i] + θ_2[i]) + L[2] * np.cos(θ_1[i] + θ_2[i] + θ_3)
        z_reverse = L[0] * np.sin(θ_1[i]) + L[1] * np.sin(θ_1[i] + θ_2[i]) + L[2] * np.sin(θ_1[i] + θ_2[i] + θ_3)

        # 目標値との誤差
        error_x = x_target - x_reverse
        error_z = z_target - z_reverse
        error = np.sqrt(error_x**2 + error_z**2)
    
        #print(Color.GREEN, f"目標 ({x_target:.1f}, {z_target:1f}): θ_1 = {np.rad2deg(θ_1[i]):.2f}, θ_2 = {np.rad2deg(θ_2[i]):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}", Color.RESET, sep = '')
        #print(Color.GREEN, f"到達 ({x_reverse:.3f}, {z_reverse:.3f})", Color.RESET, sep = '')

    """

    θ_3 = w * np.pi/2 - θ_1 - θ_2

    # 角度の正規化
    θ_1, θ_2, θ_3 = clean.normalization1(θ_1, θ_2, θ_3)
    x_reverse = L[0] * np.cos(θ_1) + L[1] * np.cos(θ_1 + θ_2) + L[2] * np.cos(θ_1 + θ_2 + θ_3)
    z_reverse = L[0] * np.sin(θ_1) + L[1] * np.sin(θ_1 + θ_2) + L[2] * np.sin(θ_1 + θ_2 + θ_3)    

    print(f"θ_rad = {θ_1}, {θ_2}, {θ_3}")

    # 目標値との誤差
    error_x = x_target - x_reverse
    error_z = z_target - z_reverse
    error = np.sqrt(error_x**2 + error_z**2)

    # データをリストに追加
    data_i = [L[0], L[1], L[2], x_target, z_target, True, θ_1, θ_2, θ_3, error]
    data.append (data_i)

    print(Color.GREEN, f"目標 ({x_target:.1f}, {z_target:1f}): θ_1 = {np.rad2deg(θ_1):.2f}, θ_2 = {np.rad2deg(θ_2):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}", Color.RESET, sep = '')
    print(Color.GREEN, f"到達 ({x_reverse:.3f}, {z_reverse:.3f})", Color.RESET, sep = '')

    return(data)


# for文で目標座標をズラして各目標座標から角度を計算し、誤差を検証
# loop1では目標座標と誤差を検証
def keisan_loop1(L, w):
    data = []
    for z_target in np.arange(-5.0, 5.1, 0.001):
        print(Color.BLUE, f"{z_target:.3f}", Color.RESET, sep = '')
        for x_target in np.arange(-5.0, 5.1, 0.001):
            start_time = datetime.now()
                     
            x_target, z_target = clean.truncate(x_target, z_target)

            x_2 = x_target - L[2] * np.cos(w * np.pi / 2)
            z_2 = z_target - L[2] * np.sin(w * np.pi / 2)

            # 到達可能か？
            u = x_2**2 + z_2**2
            l = np.sqrt(u)

            if L[0] + L[1] < l:
                #print(f"目標 ({x_target:.1f}, {z_target}) は到達不可能です。")

                # データをリストに追加
                data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
                continue

            cosθ_2 = (u - L[0]**2 - L[1]**2 ) / (2 * L[0] * L[1] )
            
            if not -1 <= cosθ_2 <= 1:
                print(f"目標 ({x_target:.3f}, {z_target:.3f}) は到達不可能です。")

                # データをリストに追加
                data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
                return(data)

            θ_2_1 = np.arccos(cosθ_2) #+ np.pi/8
            θ_2_2 = -θ_2_1
            θ_2_3 = np.pi - θ_2_1
            θ_2_4 = np.pi - θ_2_2
            θ_2_5 = θ_2_1 + np.pi/2
            θ_2_6 = θ_2_2 + np.pi/2
            θ_2_7 = θ_2_3 + np.pi/2
            θ_2_8 = θ_2_4 + np.pi/2

            θ_2_kouho2 = [θ_2_1, θ_2_2, θ_2_3, θ_2_4, θ_2_5, θ_2_6, θ_2_7, θ_2_8]

            φ_2 = np.arctan2(x_2, z_2 )
            cosθ_1u = (u + L[0]**2 - L[1]**2) / (2 * L[0] * l)

            if not -1 <= cosθ_1u <= 1:
                print(f"目標 ({x_target:.3f}, {z_target:.3f}) は到達不可能です。")

            # データをリストに追加
                data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])
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

            θ_1_kouho2 = [θ_1_1, θ_1_2, θ_1_3, θ_1_4, θ_1_5, θ_1_6, θ_1_7, θ_1_8, θ_1_9, θ_1_10, θ_1_11, θ_1_12, θ_1_13, θ_1_14, θ_1_15, θ_1_16]

            θ_1_kouho, θ_2_kouho, θ_x = clean.normalization2(θ_1_kouho2, θ_2_kouho2, None)
            

            θ_1, θ_2 = thetachoice.choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w)
            #pdb.set_trace()

            # print (f"θ_1_kouho = {θ_1}, θ_2_kouho = {θ_2}")

            # end_time = datetime.now()
            # elapsed_time = end_time - start_time
            # print(Color.YELLOW ,f"16所要時間 = {elapsed_time}", Color.RESET)

            if θ_1 == None or θ_2 == None:
                print(f"目標 ({x_target:.3f}, {z_target:.3f}) は到達不可能です。")
                continue

            # データをリストに追加
            data.append([L[0], L[1], L[2], x_target, z_target, False, "None", "None", "None", "None"])

            θ_3 = w * np.pi/2 - θ_1 - θ_2

            # 角度の正規化
            #pdb.set_trace()
            θ_1, θ_2, θ_3 = clean.normalization1(θ_1, θ_2, θ_3)
            #pdb.set_trace()

            x_reverse = L[0] * np.cos(θ_1) + L[1] * np.cos(θ_1 + θ_2) + L[2] * np.cos(θ_1 + θ_2 + θ_3)
            z_reverse = L[0] * np.sin(θ_1) + L[1] * np.sin(θ_1 + θ_2) + L[2] * np.sin(θ_1 + θ_2 + θ_3)

            # 目標値との誤差
            error_x = x_target - x_reverse
            error_z = z_target - z_reverse
            error = np.sqrt(error_x**2 + error_z**2)

            #pdb.set_trace()
            print(Color.GREEN, f"目標 ({x_target:.3f}, {z_target:.3f}): θ_1 = {np.rad2deg(θ_1):.2f}, θ_2 = {np.rad2deg(θ_2):.2f}, θ_3 = {np.rad2deg(θ_3):.2f}, error = {error:.2f}" ,Color.RESET, sep = '')

            data_i = [L[0], L[1], L[2], x_target, z_target, True, θ_1, θ_2, θ_3, error]
            data.append (data_i)

            #print(len(data))

            end_time = datetime.now()
            print(f"所要時間_calcu_loop = {end_time - start_time}")

    return(data)