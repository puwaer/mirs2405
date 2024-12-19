import torch
import torch.nn as nn
import torchvision.transforms as transforms
import cv2
import numpy as np

# モデルのインポート
from torchvision.models import resnet50
from facenet_pytorch import MTCNN, InceptionResnetV1

class EmotionRecognitionModel(nn.Module):
    def __init__(self, num_classes=7):
        super(EmotionRecognitionModel, self).__init__()
        # ResNet50をベースモデルとして使用
        self.base_model = resnet50(pretrained=True)
        
        # 最終層を置き換える
        num_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
        # 感情クラス
        self.emotion_classes = [
            'angry', 'disgust', 'fear', 'happy', 
            'sad', 'surprise', 'neutral'
        ]
    
    def forward(self, x):
        return self.base_model(x)
    
    def predict_emotion(self, x):
        with torch.no_grad():
            outputs = self.forward(x)
            _, predicted = torch.max(outputs, 1)
            return self.emotion_classes[predicted.item()]

class AgeGenderRecognitionModel(nn.Module):
    def __init__(self):
        super(AgeGenderRecognitionModel, self).__init__()
        # ResNet50をベースモデルとして使用
        self.base_model = resnet50(pretrained=True)
        
        # 年齢と性別の推定のためのヘッド
        num_features = self.base_model.fc.in_features
        self.age_head = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 1)  # 年齢を回帰問題として扱う
        )
        
        self.gender_head = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 2)  # 2クラス分類（男性/女性）
        )
    
    def forward(self, x):
        features = self.base_model(x)
        age = self.age_head(features)
        gender = self.gender_head(features)
        return age, gender

class FaceAnalyzer:
    def __init__(self, device=None):
        # デバイスの設定
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 顔検出モデル
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        
        # モデルの初期化と重みのロード
        self.emotion_model = EmotionRecognitionModel().to(self.device)
        self.age_gender_model = AgeGenderRecognitionModel().to(self.device)
        
        # プリトレーニング済みの重みをロード（実際のパスに置き換える）
        # self.emotion_model.load_state_dict(torch.load('emotion_model_weights.pth'))
        # self.age_gender_model.load_state_dict(torch.load('age_gender_model_weights.pth'))
        
        # 前処理の設定
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def preprocess_face(self, frame):
        # 顔検出
        boxes, _ = self.mtcnn.detect(frame)
        
        if boxes is None or len(boxes) == 0:
            return None, None
        
        # 最初の顔を選択
        box = boxes[0].astype(int)
        x1, y1, x2, y2 = box
        
        # 顔画像の切り出し
        face = frame[y1:y2, x1:x2]
        
        # 前処理
        face_tensor = self.transform(face).unsqueeze(0).to(self.device)
        
        return face_tensor, (x1, y1, x2, y2)
    
    def recognize_emotion(self, face_tensor):
        if face_tensor is None:
            return "Unknown"
        
        self.emotion_model.eval()
        emotion = self.emotion_model.predict_emotion(face_tensor)
        return emotion
    
    def recognize_age_gender(self, face_tensor):
        if face_tensor is None:
            return None, None
        
        self.age_gender_model.eval()
        with torch.no_grad():
            age, gender = self.age_gender_model(face_tensor)
            
            # 年齢の調整（モデルによって異なる可能性があるため）
            age = int(torch.clamp(age, min=0, max=100).item())
            
            # 性別の推定
            gender_idx = torch.argmax(gender, dim=1).item()
            gender_label = "Male" if gender_idx == 0 else "Female"
        
        return age, gender_label

def main():
    # カメラの初期化
    cap = cv2.VideoCapture(0)  # セカンダリカメラ（必要に応じて調整）
    
    # FaceAnalyzerの初期化
    analyzer = FaceAnalyzer()
    
    while True:
        # フレームの読み込み
        ret, frame = cap.read()
        if not ret:
            break
        
        # 顔の検出と前処理
        face_tensor, face_box = analyzer.preprocess_face(frame)
        
        if face_tensor is not None and face_box is not None:
            # 表情認識
            try:
                emotion = analyzer.recognize_emotion(face_tensor)
                x1, y1, x2, y2 = face_box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Emotion: {emotion}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            except Exception as e:
                print("表情認識エラー:", str(e))
            
            # 年齢・性別認識
            try:
                age, gender = analyzer.recognize_age_gender(face_tensor)
                if age is not None and gender is not None:
                    cv2.putText(frame, f"Age: {age}, Gender: {gender}", 
                                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            except Exception as e:
                print("年齢・性別認識エラー:", str(e))
        
        # フレームの表示
        cv2.imshow("PyTorch Face Analysis", frame)
        
        # 終了条件
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # リソースの解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# 注意: このスクリプトは、実際の学習済みモデルの重みをロードする必要があります。
# 以下のライブラリが必要です:
# pip install torch torchvision opencv-python facenet-pytorch
