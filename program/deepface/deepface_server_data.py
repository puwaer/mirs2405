import cv2
from deepface import DeepFace
import numpy as np
import socketserver
import json
import sys

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # 辞書をJSON文字列に変換
            json_str = json.dumps(self.server.current_data)
            
            # 文字列をバイト列に変換
            data = json_str.encode('utf-8')
            
            # データサイズを取得
            size = len(data).to_bytes(4, byteorder='big')
            
            # サイズとデータを送信（1回だけ）
            self.request.sendall(size + data)
            
        except ConnectionError:
            print("Connection lost")
        except Exception as e:
            print(f"Error occurred: {e}")

class CustomTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.current_data = None
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)



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
    # DeepFaceのdetect_face関数で顔検出を行う
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
    
def start_server(HOST, PORT, input_text) :
    socketserver.TCPServer.allow_reuse_address = True
    server = CustomTCPServer((HOST, PORT), TCPHandler)

    try:
        print("Server started")
        while True:
            
            # 入力されたデータを保存
            server.current_data = input_text
            
            # クライアントからの接続を1回待ち受ける
            server.handle_request()
            
            print("Data sent. Waiting for next input...")
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()
        sys.exit()


def main(HOST, PORT):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 顔検出とバウンディングボックスの取得
        bbox = get_face_bbox(frame)
        if bbox:
            x, y, w, h = bbox
            # バウンディングボックスを描画（緑色）
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        # 年齢推定
        try:
            estimated_age = age_analysis(frame)
            cv2.putText(frame, f"Age: {estimated_age}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(estimated_age)
            start_server(HOST, PORT, estimated_age)
        except Exception as e:
            print("年齢推定エラー:", str(e))

        # 性別推定
        try:
            estimated_gender = gender_analysis(frame)
            cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(estimated_gender)
        except Exception as e:
            print("性別推定エラー:", str(e))

        # 映像を表示
        cv2.imshow("Face Recognition & Analysis", frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    HOST = '172.25.15.27'
    PORT = 5700
    main(HOST, PORT)