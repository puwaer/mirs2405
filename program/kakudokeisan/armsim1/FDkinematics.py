import numpy as np
import pdb

from color import Color


def Forward_Kinematics(L, θ_1, θ_2, θ_3):
    x_3 = L[0] * np.cos(θ_1 + θ_2 + θ_3) + L[1] * np.cos(θ_1 + θ_2 + θ_3) + L[2] * np.cos(θ_1 + θ_2 + θ_3)
    z_3 = L[0] * np.sin(θ_1 + θ_2 + θ_3) + L[1] * np.sin(θ_1 + θ_2 + θ_3) + L[2] * np.sin(θ_1 + θ_2 + θ_3)
    return(x_3, z_3)

def FD_All(L, θ_1, θ_2, θ_3):
    #pdb.set_trace()
    x_1 = L[0] * np.cos(θ_1)
    z_1 = L[0] * np.sin(θ_1)
    x_2 = x_1 + L[1] * np.cos(θ_1 + θ_2)
    z_2 = z_1 + L[1] * np.sin(θ_1 + θ_2)
    x_3 = x_2 + L[2] * np.cos(θ_1 + θ_2 + θ_3)
    z_3 = z_2 + L[2] * np.sin(θ_1 + θ_2 + θ_3)

    X = [x_1, x_2, x_3]
    Z = [z_1, z_2, z_3]

    # print(f"x_1 = {x_1}, x_2 = {x_2}, x_3 = {x_3}, z_1 = {z_1}, z_1 = {z_2}, z_1 = {z_3},")
    # print(f"{Color.BLUE}θ_1 = {θ_1}, θ_2 = {θ_2}, θ_3 = {θ_3}, {Color.RESET}", sep = '')

    return(X, Z)