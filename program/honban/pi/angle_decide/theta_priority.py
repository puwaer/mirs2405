import numpy as np
import theta_priority

#import pdb
#from color import Color


# どのθの組を選ぶか
def priority(θ_1_kouho, θ_2_kouho, r, indices, w):
    r_min = np.min(r)                                                  # 誤差が最小な要素の取得
    r_min_indices = np.where(r == r_min)[0]                            # 誤差が最小な要素のインデックスを取得

    # 誤差が最小な組が複数ある時 + 渡すときだけ考慮
    if (len(r_min_indices) != 1) and (w == 1):
        θ_1_kouho_2 = []
        θ_2_kouho_2 = []

        for k in range(len(r_min_indices)):                            # 誤差が最小の組だけのθの候補を生成
            i, j = indices[r_min_indices[k]]
            θ_1_kouho_2.append(θ_1_kouho[i])
            θ_2_kouho_2.append(θ_2_kouho[j])

        # θ_1が最も30°に近い候補を選ぶ
        nearest_index = min(range(len(θ_1_kouho_2)),key=lambda i: abs(θ_1_kouho_2[i] - np.pi/6))
        θ_1_choiced = θ_1_kouho_2[nearest_index]
        θ_2_choiced = θ_2_kouho_2[nearest_index]

    # その他の時は考慮しない。配列で要素が早い方を選ぶ。
    else:
        k = np.argmin(r_min)
        i, j = indices[k]
        θ_1_choiced = θ_1_kouho[i]
        θ_2_choiced = θ_2_kouho[j]

    return(θ_1_choiced, θ_2_choiced)