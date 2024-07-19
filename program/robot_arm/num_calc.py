#ロボットアーム数値計算

#順運動学の式を求める関数
def FK(L, js):
  Ts = []
  c0 = math.cos(js[0])
  s0 = math.sin(js[0])
  c1 = math.cos(js[1])
  s1 = math.sin(js[1])
  c2 = math.cos(js[2])
  s2 = math.sin(js[2])
  c3 = math.cos(js[3])
  s3 = math.sin(js[3])
  c4 = math.cos(js[4])
  s4 = math.sin(js[4])
  c5 = math.cos(js[5])
  s5 = math.sin(js[5])

  Ts.append(np.matrix([[c0, -s0, 0, 0], [s0, c0, 0, 0], [0, 0, 1, L[0]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[1, 0, 0, 0], [0, c1, -s1, -0.03], [0, s1, c1, L[1]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[1, 0, 0, 0], [0, c2, -s2, 0], [0, s2, c2, L[2]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[c3, -s3, 0, 0], [s3, c3, 0, 0], [0, 0, 1, L[3]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[1, 0, 0, 0], [0, c4, -s4, 0], [0, s4, c4, L[4]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[c5, -s5, 0, 0], [s5, c5, 0, 0], [0, 0, 1, L[5]], [0, 0, 0, 1]]))
  Ts.append(np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, L[6]], [0, 0, 0, 1]]))

  return [Ts[0], Ts[0]*Ts[1], Ts[0]*Ts[1]*Ts[2], Ts[0]*Ts[1]*Ts[2]*Ts[3], Ts[0]*Ts[1]*Ts[2]*Ts[3]*Ts[4],
          Ts[0]*Ts[1]*Ts[2]*Ts[3]*Ts[4]*Ts[5], Ts[0]*Ts[1]*Ts[2]*Ts[3]*Ts[4]*Ts[5]*Ts[6]]

# クォータニオンを生成する関数
def make_q(L, theta):
  return [L[0]*math.sin(theta/2), L[1]*math.sin(theta/2), L[2]*math.sin(theta/2), math.cos(theta/2)]

# クォータニオンの積を計算する関数
def my_cross(q, p):
  return [q[3]*p[0] - q[2]*p[1] + q[1]*p[2] + q[0]*p[3],
          q[2]*p[0] + q[3]*p[1] - q[0]*p[2] + q[1]*p[3],
          -q[1]*p[0] + q[0]*p[1] + q[3]*p[2] + q[2]*p[3],
          -q[0]*p[0] - q[1]*p[1] - q[2]*p[2] + q[3]*p[3]]

# 各関節角度から手先姿勢を求める関数
def check_q(Theta):
  s53_0 = math.sin(Theta[5]/2 + Theta[3]/2 - Theta[0]/2)
  c53_0 = math.cos(Theta[5]/2 + Theta[3]/2 - Theta[0]/2)
  s5_3_0 = math.sin(Theta[5]/2 - Theta[3]/2 - Theta[0]/2)
  c5_3_0 = math.cos(Theta[5]/2 - Theta[3]/2 - Theta[0]/2)
  s3_0_5 = math.sin(Theta[3]/2 - Theta[0]/2 - Theta[5]/2)
  c3_0_5 = math.cos(Theta[3]/2 - Theta[0]/2 - Theta[5]/2)
  s530 = math.sin(Theta[5]/2 + Theta[3]/2 + Theta[0]/2)
  c530 = math.cos(Theta[5]/2 + Theta[3]/2 + Theta[0]/2)
  s12 = math.sin(Theta[1]/2 + Theta[2]/2)
  c12 = math.cos(Theta[1]/2 + Theta[2]/2)
  s4 = math.sin(Theta[4]/2)
  c4 = math.cos(Theta[4]/2)

  return [c53_0*c4*s12 + c5_3_0*s4*c12,
          -s53_0*c4*s12 - s5_3_0*s4*c12,
          s3_0_5*s4*s12 + s530*c4*c12,
          -c3_0_5*s4*s12 + c530*c4*c12]

# θの範囲を[-π, π]に直す関数
def fixPi(Js):
  js = Js
  for j in range(len(Js)):
    if js[j] > math.pi:
      js[j] = js[j] - int((js[j] + math.pi)/(2*math.pi))*2*math.pi
    elif js[j] < -math.pi:
      js[j] = js[j] - int((js[j]-math.pi)/(2*math.pi))*2*math.pi
  return js
