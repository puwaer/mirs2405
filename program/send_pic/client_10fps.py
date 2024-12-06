import socket
import numpy
import cv2
import time

HOST = "172.25.16.100"  # サーバーのIPアドレスaaa
PORT = 5569
TARGET_FPS = 10  # 目標FPS
FRAME_INTERVAL = 1 / TARGET_FPS  # フレーム間隔 (秒)


def getimage(sock):
    size = int.from_bytes(sock.recv(4), byteorder='big')  # データサイズを受信
    buf = b''
    while len(buf) < size:  # 全データを受信
        buf += sock.recv(size - len(buf))
    recdata = numpy.frombuffer(buf, dtype='uint8')
    return cv2.imdecode(recdata, 1)  # 画像データにデコード


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# FPS計算用の変数
frame_count = 0
start_time = time.time()
fps = 0.0  # 初期値

while True:
    loop_start_time = time.time()  # ループ開始時間

    img = getimage(sock)
    if img is None:
        continue

    # フレーム数をカウント
    frame_count += 1
    elapsed_time = time.time() - start_time

    # 1秒経過ごとにFPSを計算
    if elapsed_time > 1.0:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()

    # FPSを画面に表示
    cv2.putText(
        img,                         # 描画対象の画像
        f"FPS: {fps:.2f}",           # 表示する文字列
        (10, 30),                    # 表示位置 (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,    # フォント
        1,                           # フォントスケール
        (0, 255, 0),                 # 色 (B, G, R)
        2                            # 太さ
    )

    cv2.imshow('Capture', img)

    # 終了条件
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # ループの終了時間を計算して待機
    loop_end_time = time.time()
    loop_duration = loop_end_time - loop_start_time
    if loop_duration < FRAME_INTERVAL:
        time.sleep(FRAME_INTERVAL - loop_duration)

sock.close()
cv2.destroyAllWindows()
