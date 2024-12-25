import numpy as np
#import pdb

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