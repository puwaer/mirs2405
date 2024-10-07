import cv2
from deepface import DeepFace

# 顔認証のためのユーザー情報（顔画像へのパス）
user_image_path = "path_to_user_image.jpg"

# 表情推定を行う関数
def emotion_analysis(image):
    result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    return result[0]['dominant_emotion']

# 年齢推定を行う関数
def age_analysis(image):
    result = DeepFace.analyze(image, actions=['age'], enforce_detection=False)
    return result[0]['age']

# 性別推定を行う関数
def gender_analysis(image):
    result = DeepFace.analyze(image, actions=['gender'], enforce_detection=False)
    return result[0]['gender']

# メイン処理
def main():
    # カメラからの映像を取得
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # DeepFaceで顔認証
        """
        try:
            result = DeepFace.verify(frame, user_image_path, enforce_detection=False)
            print(f"認証結果: {result['verified']}")
        except Exception as e:
            print("顔認証エラー:", str(e))
        
        # 表情推定
        try:
            dominant_emotion = emotion_analysis(frame)
            cv2.putText(frame, f"Emotion: {dominant_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        except Exception as e:
            print("表情推定エラー:", str(e))
        """
            
        # 年齢推定
        try:
            estimated_age = age_analysis(frame)
            cv2.putText(frame, f"Age: {estimated_age}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(estimated_age)
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
        cv2.imshow("Face Recognition & Emotion Analysis", frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
