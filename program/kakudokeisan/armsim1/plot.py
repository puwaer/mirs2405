import os
import matplotlib.pyplot as plt
import pdb

import FDkinematics
from color import Color


# 順運動学でグラフにプロット
def fig_plot(data):
    #pdb.set_trace()
    for i in range (len(data)):
        data_i = data[i]

        if data_i[5] == False:
            continue

        L = [data_i[0], data_i[1], data_i[2]]
        θ_1 = data_i[6]
        θ_2 = data_i[7]
        θ_3 = data_i[8]

        X, Z = FDkinematics.FD_All(L, θ_1, θ_2, θ_3)

        X.insert(0, 0)
        Z.insert(0, 0)

        #print(f"len(data) = {len(data)}")
        #print(f"len(X) = {len(X)}")
        #print(f"len(Z) = {len(Z)}")

        # print(f"{Color.YELLOW}θ_1 = {θ_1_deg}, θ_2 = {θ_2_deg}, θ_3 = {θ_3_deg} {Color.RESET}")
        # print(f"{Color.YELLOW}X = {X}, Z = {Z} {Color.RESET}")

        # アーム全体を描画
        color = ["blue", "green", "red"]
        for j in range (0, 3, 1):
            pX = [X[j], X[j+1]]
            pZ = [Z[j], Z[j+1]]
            plt.plot(pX, pZ, color = color[j])
            # plt.plot(X[j], Z[j], marker='o', color = 'black')
            plt.plot(X[3], Z[3], marker='o', color = 'yellow')

    plt.axhline(0, color="black", linewidth=0.8)  # X軸
    plt.axvline(0, color="black", linewidth=0.8)  # Z軸
    plt.xlabel("X-axis")
    plt.ylabel("Z-axis")
    plt.title("Arm Configuration at Current Target")
    plt.grid(True)
    #plt.legend()
    plt.grid(True)

    plt.show ()
    plt.close()  # 図を閉じてメモリを解放

    return()


    # 順運動学でグラフにプロット
def fig_png(data):
    #pdb.set_trace()
    for i in range (len(data)):
        data_i = data[i]

        if data_i[5] == False:
            continue

        L = [data_i[0], data_i[1], data_i[2]]
        θ_1 = data_i[6]
        θ_2 = data_i[7]
        θ_3 = data_i[8]

        X, Z = FDkinematics.FD_All(L, θ_1, θ_2, θ_3)

        X.insert(0, 0)
        Z.insert(0, 0)

        # print(f"{Color.YELLOW}θ_1 = {θ_1_deg}, θ_2 = {θ_2_deg}, θ_3 = {θ_3_deg} {Color.RESET}")
        # print(f"{Color.YELLOW}X = {X}, Z = {Z} {Color.RESET}")

        # アーム全体を描画
        color = ["blue", "green", "red"]
        for j in range (0, 3, 1):
            pX = [X[j], X[j+1]]
            pZ = [Z[j], Z[j+1]]
            plt.plot(pX, pZ, color = color[j])
            # plt.plot(X[j], Z[j], marker='o', color = 'black')
            plt.plot(X[3], Z[3], marker='o', color = 'yellow')

    plt.axhline(0, color="black", linewidth=0.8)  # X軸
    plt.axvline(0, color="black", linewidth=0.8)  # Z軸
    plt.xlabel("X-axis")
    plt.ylabel("Z-axis")
    plt.axis('scaled')
    plt.title("Arm Configuration at Current Target")
    plt.grid(True)
    #plt.legend()
    plt.grid(True)

    # PNGとして保存
    save = os.path.join("fig", "Arm_Configuration_at_Current_Target_nazo.png")
    if not os.path.exists("fig"):
        os.makedirs("fig")
    
    plt.savefig(save, dpi=800)  # dpiは解像度、必要に応じて調整
    
    plt.close()  # 図を閉じてメモリを解放
    print("結果をPNG形式で保存しました。")

    return()