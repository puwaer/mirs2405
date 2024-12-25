import numpy as np
import random

from color import Color
import thetachoice, clean

L = [0.5, 0.5, 0.1]  # 各リンクの長さ
x_target, z_target = 0.5, 0.5  # 目標座標
i = random.randint(10, 20)
θ_1 = []
θ_2 = []

for j in range (1, i, 1):
    θ_1_1 = random.uniform(-100, 100)
    θ_2_1 = random.uniform(-100, 100)
    θ_1.append(θ_1_1)
    θ_2.append(θ_2_1)

print(i)
print(f"θ_1 = {θ_1}")
print(f"Θ_2 = {θ_2}")

thetachoice.choicetheta_matrix(L, None, None, θ_1, θ_2, x_target, z_target)
# θ_3_1 = -3/2 * np.pi

# θ_1, θ_2, θ_3 = clean.normalization(θ_1_1, θ_2_1, θ_3_1)

#print("θ_1 = ", θ_1, "θ_2 = ", θ_2, "θ_3 = ", θ_3)