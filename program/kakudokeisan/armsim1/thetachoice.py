import numpy as np
from multiprocessing import Pool
import pdb

from color import Color


def choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w):
    r = []
    indicies = []
    c = 0

    for i in range (len(θ_1_kouho)):
        for j in range (len(θ_2_kouho)):
            x_kouho = L[0] * np.cos(θ_1_kouho[i]) + L[1] * np.cos(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.cos(w * np.pi/2)
            z_kouho = L[0] * np.sin(θ_1_kouho[i]) + L[1] * np.sin(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.sin(w * np.pi/2)

            if np.sign(x_kouho) != np.sign(x_target) or np.sign (z_kouho) != np.sign(z_target):
                c += 1
                #print(f"この候補を棄却しました。({c}回目)")
                continue

            x_r = x_target - x_kouho
            z_r = z_target - z_kouho

            r_kouho = np.sqrt (x_r**2 + z_r**2)

            r.append(r_kouho)
            indicies.append([i, j])

    if c == len(θ_1_kouho) * len(θ_2_kouho):
        return(None, None)

    k = np.argmin(r)
    i, j = indicies[k]
    θ_1_choiced = θ_1_kouho[i]
    θ_2_choiced = θ_2_kouho[j]

    return(θ_1_choiced, θ_2_choiced)

def choicetheta2(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w):
    indicies = []
    θ_1_choiced = []
    θ_2_choiced = []
    c = 0

    for i in range (len(θ_1_kouho)):
        for j in range (len(θ_2_kouho)):
            x_kouho = L[0] * np.cos(θ_1_kouho[i]) + L[1] * np.cos(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.cos(w * np.pi/2)
            z_kouho = L[0] * np.sin(θ_1_kouho[i]) + L[1] * np.sin(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.sin(w * np.pi/2)

            """
            if np.sign(x_kouho) != np.sign(x_target) or np.sign (z_kouho) != np.sign(z_target):
                c += 1
                print(f"x_3 = {x_kouho}, z_3 = {z_kouho}")
                print(f"この候補を棄却しました。({c}回目)")
                continue
            """

            #print(Color.YELLOW, f"x_3 = {x_kouho}, z_3 = {z_kouho}", Color.RESET, sep = '')
            indicies.append([i, j])

    if c >= len(θ_1_kouho) * len(θ_2_kouho):
        return(None, None)

    for i in range (len(indicies)):
        a, b = indicies[i]
        θ_1_choiced.append(θ_1_kouho[a])
        θ_2_choiced.append(θ_2_kouho[b])

    return(θ_1_choiced, θ_2_choiced)


def choicetheta_matrix(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w):
    
    # NumPyの表示設定を変更して最大精度で出力
    np.set_printoptions(precision=16, floatmode='maxprec', suppress=False)

    # メッシュグリッドの作成
    θ_1_grid, θ_2_grid = np.meshgrid(θ_1_kouho, θ_2_kouho)
    θ_matrix = np.stack([
        θ_1_grid.ravel(), 
        (θ_1_grid + θ_2_grid).ravel(), 
        -np.pi * np.ones_like(θ_1_grid).ravel()
    ], axis=1)

    #pdb.set_trace()
    θ_matrix = np.array(θ_matrix)

    # X_matrixとZ_matrixの計算
    X_matrix = np.sum(L * np.cos(θ_matrix), axis=1)
    Z_matrix = np.sum(L * np.sin(θ_matrix), axis=1)

    # X_matrixとZ_matrixを個別に確認
    print("X_matrix:")
    for x in X_matrix:
        print(f"{x:.16e}")  # 科学技術表記で表示

    print("Z_matrix:")
    for z in Z_matrix:
        print(f"{z:.16e}")  # 科学技術表記で表示

    # 差分と距離の計算
    X_r = X_matrix - x_target
    Z_r = Z_matrix - z_target
    R_matrix = np.sqrt(X_r**2 + Z_r**2)

    # 最小値のインデックスとθの選択
    k = np.argmin(R_matrix)
    θ_choiced = θ_matrix[k]

    # R_matrixを確認
    print("R_matrix:")
    for r in R_matrix:
        print(f"{r:.16e}")  # 科学技術表記で表示

    return (θ_choiced[0], θ_choiced[1])

