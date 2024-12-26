import numpy as np

#import pdb
#from color import Color


# θの範囲を -πからπ にする。 (θはスカラー)
def normalization1(θ_1, θ_2, θ_3):
    ψ = [θ_1, θ_2, θ_3]
    #pdb.set_trace()

    for i in range(len(ψ)):
        θ_i = ψ[i]
        if θ_i == None:
            continue

        θ_i = np.fmod(θ_i, 2 * np.pi)
            
        if θ_i == -np.pi:      # θが-πの時: θをπに変換
            θ_i = np.pi 

        elif θ_i > np.pi:      # θが正+第3,4象限の時: θを0から-πの負に変換
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

            if θ_i[j] == -np.pi:      # θが-πの時: θをπに変換
                θ_i[j] = np.pi 

            elif θ_i[j] > np.pi:        # θが正+第3,4象限の時: θを0から-πの負に変換
                θ_i[j] -= 2 * np.pi

            elif θ_i[j] < -np.pi:     # Θが負+第1,2象限の時: θを0からpiの正に変換
                θ_i[j] += 2 * np.pi

    return (ψ[0], ψ[1], ψ[2])


def theta_convers(data):
    if data[0] != True:
        return(None, None)

    θ_1 = data[1]
    θ_2 = data[2]
    θ_2 += θ_1

    θ_1, θ_2, dont_use = normalization1(θ_1, θ_2, None)
            
    # pdb.set_trace()

    if -np.pi < θ_1 <= np.pi:
        φ_1 = np.pi/2 - θ_1
    else:
        print(f"θ_1 is ERROR! : {np.rad2deg(θ_1)}")
        return

    if -np.pi < θ_2 <= np.pi:
        φ_2 = np.pi/2 - θ_2
    else:
        print(f"θ_2 is ERROR! : {np.rad2deg(θ_2)}")
        return

    #print(Color.YELLOW, f"φ_1 = {np.rad2deg(θ_1)}, φ_2 = {np.rad2deg(θ_2)}", sep='')
    return(φ_1, φ_2)