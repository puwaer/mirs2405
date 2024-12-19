import socket
import cv2
from deepface import DeepFace
import numpy as np
import json
import time
import threading
import queue
import socketserver

# サーバー接続設定
#HOST = "172.25.16.100"  # 画像送信元サーバー
HOST = "172.25.18.20"  # 画像送信元サーバー
PORT = 5585  # 画像送信元ポート
SERVER_HOST = "172.25.16.100"  # 結果送信先サーバー
SERVER_PORT = 5700  # 結果送信先ポート

# 最新の画像を管理するキュー
image_queue = queue.Queue(maxsize=1)

# グローバル変数として最新の推定結果を保持
latest_results = {
    'age': None,
    'gender': None,
    'time': 0
}

def get_image(sock):
    """
    ソケットから画像データを受信する関数
    
    Args:
        sock (socket.socket): 接続されたソケット
    
    Returns:
        numpy.ndarray: 受信した画像
    """
    # 画像サイズを受信
    size = int.from_bytes(sock.recv(4), byteorder='big')
    
    # 画像データを受信
    buf = b''
    while len(buf) < size:
        buf += sock.recv(size - len(buf))
    
    # 画像をデコード
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
            # 最新の画像を受信
            img = get_image(sock)
            
            # キューが満杯の場合、古い画像を削除
            if image_queue.full():
                try:
                    image_queue.get_nowait()
                except queue.Empty:
                    pass
            
            # 新しい画像をキューに追加
            image_queue.put(img)
        
        except Exception as e:
            print("画像受信エラー:", str(e))
            break

def start_server(host, port):
    class TCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            while True:
                try:
                    # 最新の推定結果をJSONとして送信
                    data_dict = {
                        'age': latest_results['age'],
                        'gender': latest_results['gender'],
                        'time': latest_results['time']
                    }
                    
                    # 辞書をJSON文字列に変換
                    json_str = json.dumps(data_dict)
                    
                    # 文字列をバイト列に変換
                    data = json_str.encode('utf-8')
                    
                    # データサイズを取得
                    size = len(data).to_bytes(4, byteorder='big')
                    
                    # サイズとデータを送信
                    self.request.sendall(size + data)
                    
                    time.sleep(0.5)
                    
                except ConnectionError:
                    print("Connection lost")
                    break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    break
    
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((host, port), TCPHandler)
    print(f"Server started on {host}:{port}")
    server.serve_forever()

def emotion_analysis(image):
    result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    return result[0]['dominant_emotion']

def age_analysis(image):
    result = DeepFace.analyze(image, actions=['age'], enforce_detection=False)
    return result[0]['age']

def gender_analysis(image):
    result = DeepFace.analyze(image, actions=['gender'], enforce_detection=False)
    return result[0]['gender']

def get_face_bbox(image):
    try:
        face_objs = DeepFace.extract_faces(image, enforce_detection=False)
        if face_objs:
            face_obj = face_objs[0]
            facial_area = face_obj['facial_area']
            return (
                facial_area['x'],
                facial_area['y'],
                facial_area['w'],
                facial_area['h']
            )
    except Exception as e:
        print("顔検出エラー:", str(e))
        return None

def main():
    # サーバーを別スレッドで起動
    server_thread = threading.Thread(target=start_server, args=(SERVER_HOST, SERVER_PORT), daemon=True)
    server_thread.start()

    # ソケット接続
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"接続先: {HOST}:{PORT}")
    print("画像受信中... 'q'キーで終了")

    # 画像受信用のスレッドを開始
    receiver_thread = threading.Thread(target=image_receiver_thread, args=(sock,), daemon=True)
    receiver_thread.start()

    counter = 0

    try:
        while True:
            try:
                # キューから最新の画像を取得（待たない）
                img = image_queue.get_nowait()
                
                # 顔検出とバウンディングボックスの取得
                bbox = get_face_bbox(img)
                if bbox:
                    x, y, w, h = bbox
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    try:
                        # 年齢推定
                        estimated_age = age_analysis(img)
                        cv2.putText(img, f"Age: {estimated_age}", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # 性別推定
                        estimated_gender = gender_analysis(img)
                        cv2.putText(img, f"Gender: {estimated_gender}", (10, 110), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                        # グローバル変数を更新
                        latest_results['age'] = estimated_age
                        latest_results['gender'] = estimated_gender
                        latest_results['time'] = counter
                        counter += 1
                        print(latest_results)

                    except Exception as e:
                        print("推定エラー:", str(e))

                # 映像を表示
                cv2.imshow("Face Recognition & Analysis", img)
                
            except queue.Empty:
                # キューに画像がない場合は少し待つ
                time.sleep(0.01)

            # 終了判定
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print("エラーが発生しました:", str(e))
    
    finally:
        # リソース解放
        sock.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
