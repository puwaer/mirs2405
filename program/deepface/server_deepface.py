import cv2
from deepface import DeepFace
import numpy as np
import requests

# サーバーのIPアドレスとポート番号
HOST = '172.25.15.27'
PORT = '5000'
SERVER_URL = f"http://{HOST}:{PORT}/api"

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

def send_data_to_server(age, gender):
    try:
        payload = {"age": str(age), "gender": gender}
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            print("データ送信成功:", response.json())
        else:
            print("データ送信失敗:", response.status_code, response.text)
    except Exception as e:
        print("データ送信エラー:", str(e))

def main():
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
        except Exception as e:
            print("年齢推定エラー:", str(e))
            estimated_age = None

        # 性別推定
        try:
            estimated_gender = gender_analysis(frame)
            cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(estimated_gender)
        except Exception as e:
            print("性別推定エラー:", str(e))
            estimated_gender = None

        # サーバーにデータを送信
        if estimated_age is not None and estimated_gender is not None:
            send_data_to_server(estimated_age, estimated_gender)

        # 映像を表示
        cv2.imshow("Face Recognition & Analysis", frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
