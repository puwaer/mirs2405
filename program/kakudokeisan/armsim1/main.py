import numpy as np
from datetime import datetime

# モジュールをインポート
import theta_calcu, clean, plot, Excel
from color import Color


# 入力データ
L = [0.5, 0.5, 0.1]                                     # 各リンクの長さ
#L = [0.425, 0.426225, 0.1]
x_target, z_target = 0, 0.6                             # 目標座標
W = 1                                                   # -1 -> 掴む時 (下向き), 1 -> 渡す時 (上向き)

start_row, start_col = 2, 2                             # Excelファイルへ書き込み始めるセル

start_time = datetime.now()



#data = theta_calcu.keisan1(L, x_target, z_target, W)    # 1~3

data = theta_calcu.keisan_loop1(L, W)

end_time_1 = datetime.now()

Excel.Excel_output(data, start_row, start_col)

end_time_2 = datetime.now()

#plot.fig_plot(data)
#plot.fig_png(data)

end_time_3 = datetime.now()

φ_1, φ_2 = clean.theta_convers(data)


print(Color.GREEN, f"所要時間_calcu = {end_time_1 - start_time}", sep = '')
print(f"所要時間_Excel = {end_time_2 - end_time_1}")
#print(f"所要時間_plot = {end_time_3 - end_time_2}")
print(Color.RESET)