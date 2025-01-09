import cv2
import torch
import numpy as np
from fer import FER  # 表情推定用
from torchvision import models, transforms
from PIL import Image

# PyTorchモデルの準備（ResNetなどを使った顔の推定）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 年齢と性別推定モデルの読み込み（ここでは例としてResNetを使用）
# 代わりに事前学習済みの年齢と性別推定モデルを使うことができます
age_gender_model = models.resnet18(pretrained=True).to(device)  # 例としてResNet18
age_gender_model.eval()

# 表情推定用モデルの準備（ferライブラリ）
emotion_detector = FER()

# 年齢・性別推定関数
def age_gender_analysis(image):
    # モデルへの入力に変換
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    # 推定
    with torch.no_grad():
        outputs = age_gender_model(image_tensor)
    
    # ここではダミーとしてランダムな年齢と性別を返します
    # 実際には適切な年齢・性別推定のモデルを使って推定します
    estimated_age = np.random.randint(18, 70)
    estimated_gender = np.random.choice(['Male', 'Female'])
    
    return estimated_age, estimated_gender

# 表情推定関数
def emotion_analysis(image):
    # 表情推定
    result = emotion_detector.top_emotion(image)
    return result[0]  # dominant emotion

# メイン処理
def main():
    # カメラからの映像を取得
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # BGRからRGBに変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        # 年齢・性別推定
        try:
            estimated_age, estimated_gender = age_gender_analysis(pil_image)
            cv2.putText(frame, f"Age: {estimated_age}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print(f"Age: {estimated_age}, Gender: {estimated_gender}")
        except Exception as e:
            print("年齢・性別推定エラー:", str(e))

        # 表情推定
        try:
            dominant_emotion = emotion_analysis(frame)
            cv2.putText(frame, f"Emotion: {dominant_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            print(f"Emotion: {dominant_emotion}")
        except Exception as e:
            print("表情推定エラー:", str(e))

        # 映像を表示
        cv2.imshow("Face Recognition & Emotion Analysis", frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
