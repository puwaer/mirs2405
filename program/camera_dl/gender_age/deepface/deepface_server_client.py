import socket
import cv2
import numpy as np
from deepface import DeepFace
import json
import time
import threading
import queue
import socketserver

# サーバー設定
RECEIVE_HOST = "172.25.16.100"
RECEIVE_PORT = 5569
SEND_HOST = "172.25.16.100"
SEND_PORT = 5700

# 最新の分析結果を管理するキュー
results_queue = queue.Queue(maxsize=1)

# 画像受信用スレッドで使用するキュー
image_queue = queue.Queue(maxsize=1)

def get_image(sock):
    """
    ソケットから画像データを受信する関数
    
    Args:
        sock (socket.socket): 接続されたソケット
    
    Returns:
        numpy.ndarray: 受信した画像
    """
    size = int.from_bytes(sock.recv(4), byteorder='big')
    buf = b''
    while len(buf) < size:
        buf += sock.recv(size - len(buf))
    recdata = np.frombuffer(buf, dtype='uint8')
    return cv2.imdecode(recdata, 1)

def image_receiver_thread(sock):
    """
    画像を継続的に受信し、最新の画像のみをキューに入れるスレッド
    
    Args:
        sock (socket.socket): 接続されたソケット
    """
    while True:
        try:
            img = get_image(sock)
            if image_queue.full():
                try:
                    image_queue.get_nowait()
                except queue.Empty:
                    pass
            image_queue.put(img)
        except Exception as e:
            print("画像受信エラー:", str(e))
            break

def analyze_image(image):
    """
    画像を分析して年齢と性別を推定する関数

    Args:
        image (numpy.ndarray): 分析する画像

    Returns:
        dict: 分析結果 {"age": int, "gender": str}
    """
    try:
        result = DeepFace.analyze(image, actions=['age', 'gender'], enforce_detection=False)
        return {
            "age": result[0]['age'],
            "gender": result[0]['gender']
        }
    except Exception as e:
        print("分析エラー:", str(e))
        return {"age": None, "gender": None}

def image_processing_thread():
    """
    キューから画像を取得し、分析結果を更新するスレッド
    """
    while True:
        try:
            image = image_queue.get()
            results = analyze_image(image)
            results["time"] = time.time()

            if results_queue.full():
                try:
                    results_queue.get_nowait()
                except queue.Empty:
                    pass
            results_queue.put(results)
        except Exception as e:
            print("画像処理エラー:", str(e))

class TCPHandler(socketserver.BaseRequestHandler):
    """
    クライアントに分析結果を送信するハンドラー
    """
    def handle(self):
        while True:
            try:
                if not results_queue.empty():
                    results = results_queue.get()
                    json_str = json.dumps(results)
                    data = json_str.encode('utf-8')
                    size = len(data).to_bytes(4, byteorder='big')
                    self.request.sendall(size + data)
                    print(f"送信データ: {json_str}")
                time.sleep(0.5)
            except ConnectionError:
                print("クライアントとの接続が切れました")
                break
            except Exception as e:
                print(f"送信エラー: {e}")
                break

def start_send_server():
    """
    分析結果を送信するサーバーを起動
    """
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((SEND_HOST, SEND_PORT), TCPHandler)
    print(f"送信サーバー起動: {SEND_HOST}:{SEND_PORT}")
    server.serve_forever()

def main():
    # ソケット接続設定
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RECEIVE_HOST, RECEIVE_PORT))

    print(f"画像受信サーバー接続: {RECEIVE_HOST}:{RECEIVE_PORT}")

    # 画像受信用スレッド開始
    receiver_thread = threading.Thread(target=image_receiver_thread, args=(sock,), daemon=True)
    receiver_thread.start()

    # 画像処理スレッド開始
    processor_thread = threading.Thread(target=image_processing_thread, daemon=True)
    processor_thread.start()

    # 分析結果送信用サーバースレッド開始
    send_server_thread = threading.Thread(target=start_send_server, daemon=True)
    send_server_thread.start()

    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        print("終了します")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
