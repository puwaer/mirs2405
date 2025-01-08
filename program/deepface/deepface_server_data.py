import cv2
from deepface import DeepFace
import numpy as np
import socketserver
import json
import time
import threading

# グローバル変数として最新の推定結果を保持
latest_results = {
    'age': None,
    'gender': None,
    'time': 0
}

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

def start_server(host, port):
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
    HOST = "172.25.15.27"
    PORT = 5700
    server_thread = threading.Thread(target=start_server, args=(HOST, PORT), daemon=True)
    server_thread.start()

    cap = cv2.VideoCapture(0)
    counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 顔検出とバウンディングボックスの取得
        bbox = get_face_bbox(frame)
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            try:
                # 年齢推定
                estimated_age = age_analysis(frame)
                cv2.putText(frame, f"Age: {estimated_age}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 性別推定
                estimated_gender = gender_analysis(frame)
                cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), 
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
        cv2.imshow("Face Recognition & Analysis", frame)
        
        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()