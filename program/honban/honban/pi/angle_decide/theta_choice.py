import numpy as np
import theta_priority

#import pdb
#from color import Color


def choicetheta(L, θ_1_kouho, θ_2_kouho, x_target, z_target, w):
    r = []
    indices = []
    c = 0

    for i in range (len(θ_1_kouho)):
        for j in range (len(θ_2_kouho)):
            x_kouho = L[0] * np.cos(θ_1_kouho[i]) + L[1] * np.cos(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.cos(w * np.pi/2)
            z_kouho = L[0] * np.sin(θ_1_kouho[i]) + L[1] * np.sin(θ_1_kouho[i] + θ_2_kouho[j]) + L[2] * np.sin(w * np.pi/2)

            # 座標が象限一致していないものを弾く(目標座標が0のときは確認しない)
            # x座標
            if x_target != 0:
                if np.sign(x_kouho) != np.sign(x_target):
                    c += 1
                    #print(f"この候補を棄却しました。({c}回目)")
                    continue
            # z座標
            if z_target != 0:
                if np.sign(z_kouho) != np.sign(z_target):
                    c += 1
                    #print(f"この候補を棄却しました。({c}回目)")
                    continue
                
            x_r = x_target - x_kouho
            z_r = z_target - z_kouho

            r_kouho = np.sqrt (x_r**2 + z_r**2)

            r.append(r_kouho)
            indices.append([i, j])

    if c == len(θ_1_kouho) * len(θ_2_kouho):
        return(None, None)

    θ_1_choiced, θ_2_choiced = theta_priority.priority(θ_1_kouho, θ_2_kouho, r, indices, w)

    return(θ_1_choiced, θ_2_choiced)