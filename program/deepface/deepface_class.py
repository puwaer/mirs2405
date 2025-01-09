import cv2
from deepface import DeepFace
import numpy as np

class FaceAnalyzer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def emotion_analysis(self, image):
        try:
            result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            return result[0]['dominant_emotion']
        except Exception as e:
            print("Emotion analysis error:", str(e))
            return None

    def age_analysis(self, image):
        try:
            result = DeepFace.analyze(image, actions=['age'], enforce_detection=False)
            return result[0]['age']
        except Exception as e:
            print("Age analysis error:", str(e))
            return None

    def gender_analysis(self, image):
        try:
            result = DeepFace.analyze(image, actions=['gender'], enforce_detection=False)
            return result[0]['gender']
        except Exception as e:
            print("Gender analysis error:", str(e))
            return None

    def get_face_bbox(self, image):
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
            print("Face detection error:", str(e))
        return None

    def analyze_frame(self, frame):
        bbox = self.get_face_bbox(frame)
        estimated_age = None
        estimated_gender = None

        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        estimated_age = self.age_analysis(frame)
        if estimated_age:
            cv2.putText(frame, f"Age: {estimated_age}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        estimated_gender = self.gender_analysis(frame)
        if estimated_gender:
            cv2.putText(frame, f"Gender: {estimated_gender}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return estimated_age, estimated_gender

    def start_analysis(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            estimated_age, estimated_gender = self.analyze_frame(frame)
            data_age_gender = f"Age: {estimated_age}, Gender: {estimated_gender}"
            print(data_age_gender)

            cv2.imshow("Face Recognition & Analysis", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzer = FaceAnalyzer()
    analyzer.start_analysis()
