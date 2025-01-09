import cv2
from deepface import DeepFace
import numpy as np
import socket
import json
import threading

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

def handle_client(client_socket):
    try:
        while True:
            # 最新の推定結果をJSON形式で送信
            data = json.dumps({
                'age': estimated_age,
                'gender': estimated_gender
            })
            client_socket.send(data.encode('utf-8'))
    except Exception as e:
        print(f"クライアント処理エラー: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"サーバー起動: {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"クライアント接続: {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

def main():
    global estimated_age, estimated_gender
    estimated_age = None
    estimated_gender = None

    # サーバーを別スレッドで起動
    HOST = "172.25.15.27"
    PORT = 5700
    server_thread = threading.Thread(target=start_server, args=(HOST, PORT), daemon=True)
    server_thread.start()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        bbox = get_face_bbox(frame)
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            try:
                estimated_age = age_analysis(frame)
                cv2.putText(frame, f"Age: {estimated_age}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                estimated_gender = gender_analysis(frame)
                cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                print(f"Age: {estimated_age}, Gender: {estimated_gender}")

            except Exception as e:
                print("推定エラー:", str(e))

        cv2.imshow("Face Recognition & Analysis", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()