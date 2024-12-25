import numpy as np
import pdb

from color import Color

# 小数第二位を四捨五入 - flootの小数の計算の誤差を減らす
def truncate(x_target, z_target):
    digit = 1

    x_target = round(x_target, digit)
    z_target = round(z_target, digit)
    return (x_target, z_target)


# θの範囲を -πからπ にする。 (θはスカラー)
def normalization1(θ_1, θ_2, θ_3):
    ψ = [θ_1, θ_2, θ_3]
    #pdb.set_trace()

    for i in range(len(ψ)):
        θ_i = ψ[i]
        if θ_i == None:
            continue

        θ_i = np.fmod(θ_i, 2 * np.pi)
            
        if θ_i > np.pi:        # θが正+第3,4象限の時: θを0から-πの負に変換
            θ_i -= 2 * np.pi
                
        elif θ_i < -np.pi:     # Θが負+第1,2象限の時: θを0からπの正に変換
            θ_i += 2 * np.pi
            
    return (ψ[0], ψ[1], ψ[2])

# θの範囲を -πからπ にする。 (θは配列)
def normalization2(θ_1, θ_2, θ_3):
    ψ = [θ_1, θ_2, θ_3]
    #pdb.set_trace()

    for i in range(len(ψ)):
        θ_i = ψ[i]
        if θ_i == None:
            continue

        for j in range(len(θ_i)):
            if θ_i[j] == None:
                continue

            # 割り算の余りからθの範囲を -2πから2π にする
            θ_i[j] = np.fmod(θ_i[j], 2 * np.pi)

            if θ_i[j] > np.pi:        # θが正+第3,4象限の時: θを0から-πの負に変換
                θ_i[j] -= 2 * np.pi

            elif θ_i[j] < -np.pi:     # Θが負+第1,2象限の時: θを0からpiの正に変換
                θ_i[j] += 2 * np.pi

    return (ψ[0], ψ[1], ψ[2])


def theta_convers(data):
    φ_1 = []
    φ_2 = []

    for i in range (len(data)):
        data_i = data[i]

        # pdb.set_trace()

        if data_i[5] != True:
            continue

        θ_1 = data_i[6]
        θ_2 = data_i[7]
        θ_2 += θ_1

        θ_2 = np.fmod(θ_2, 2 * np.pi)
            
        if θ_2 > np.pi:        # θが正+第3,4象限の時: θを0から-πの負に変換
            θ_2 -= 2 * np.pi
                
        elif θ_2 < -np.pi:     # Θが負+第1,2象限の時: θを0からπの正に変換
            θ_2 += 2 * np.pi


        # pdb.set_trace()

        if 0 <= θ_1 <= np.pi:
            θ_1 = np.pi/2 - θ_1
        elif -np.pi <= θ_1 < 0 :
            θ_1 = -np.pi/2 - θ_1
        else:
            print(f"θ_1 is ERROR! : {np.rad2deg(θ_1)}")
            continue

        if 0 <= θ_2 <= np.pi:
            θ_2 = np.pi/2 - θ_2
        elif -np.pi <= θ_2 < 0 :
            θ_2 = -np.pi/2 - θ_2
        else:
            print(f"θ_2 is ERROR! : {np.rad2deg(θ_2)}")
            continue

        φ_1.append(θ_1)
        φ_2.append(θ_2)  

    print(Color.YELLOW, f"φ_1 = {np.rad2deg(φ_1)}, φ_2 = {np.rad2deg(φ_2)}", sep='')
    return(φ_1, φ_2)

def normalizationA(θ_1, θ_2, θ_3):
    def normalize_angle(angle):
        """角度を -π から π の範囲に正規化する"""
        angle = np.fmod(angle, 2 * np.pi)  # 2πで剰余を取る
        angle[angle > np.pi] -= 2 * np.pi
        angle[angle < -np.pi] += 2 * np.pi
        return angle

    def process_input(value):
        """値を正規化する。float、配列、Noneに対応"""
        if value is None:
            return None
        elif isinstance(value, (int, float)):
            value = np.array([value], dtype=float)  # 単一値を配列に変換
        elif isinstance(value, (list, np.ndarray)):
            value = np.array(value, dtype=float)   # 配列形式をNumPy配列に変換
        else:
            raise ValueError("Unsupported type for angle input.")
        normalized = normalize_angle(value)       # 正規化
        if normalized.size == 1:                  # 要素数が1ならfloatで返す
            return normalized.item()
        return normalized.tolist()                # それ以外はリストで返す

    ψ = [θ_1, θ_2, θ_3]
    ψ_normalized = [process_input(θ) for θ in ψ]
    return tuple(ψ_normalized)
