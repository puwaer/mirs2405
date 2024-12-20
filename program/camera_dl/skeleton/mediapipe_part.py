import cv2
import mediapipe as mp
import argparse

# 引数のパース
def parse_arguments():
    parser = argparse.ArgumentParser(description="mediapipeで骨格推定を実行")
    parser.add_argument('--pattern', type=str, default='pose', choices=['pose', 'hands', 'face', 'pose_hands', 'pose_face'],
                        help="使用する骨格推定のパターンを指定します。")
    return parser.parse_args()

def run_pose():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    return pose, mp_pose

def run_hands():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    return hands, mp_hands

def run_face_mesh():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    return face_mesh, mp_face_mesh

def main():
    args = parse_arguments()
    
    # 動画の読み込み (カメラを使用)
    cap = cv2.VideoCapture(1)

    # 使用する推定モデルを選択
    if args.pattern == 'pose':
        pose, mp_pose = run_pose()
    elif args.pattern == 'hands':
        hands, mp_hands = run_hands()
    elif args.pattern == 'face':
        face_mesh, mp_face_mesh = run_face_mesh()
    elif args.pattern == 'pose_hands':
        pose, mp_pose = run_pose()
        hands, mp_hands = run_hands()
    elif args.pattern == 'pose_face':
        pose, mp_pose = run_pose()
        face_mesh, mp_face_mesh = run_face_mesh()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 処理を行うための画像の前処理
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = None

        if args.pattern == 'pose':
            results = pose.process(frame_rgb)
            mp.solutions.drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS)
            cv2.imshow('MediaPipe Pose', frame)

        elif args.pattern == 'hands':
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp.solutions.drawing_styles.get_default_hand_connections_style()
                    )
            cv2.imshow("Hand Estimation", frame)

        elif args.pattern == 'face':
            results = face_mesh.process(frame_rgb)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                        connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                    )
                cv2.imshow('Face Estimation', frame)                

        elif args.pattern == 'pose_hands':
            # 両方のモデルを処理
            results_pose = pose.process(frame_rgb)
            mp.solutions.drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=results_pose.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS)
            cv2.imshow('MediaPipe Pose', frame)

            results_hands = hands.process(frame_rgb)
            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp.solutions.drawing_styles.get_default_hand_connections_style()
                    )
            cv2.imshow("Hand Estimation", frame)

        elif args.pattern == 'pose_face':
            # 両方のモデルを処理
            results_pose = pose.process(frame_rgb)
            mp.solutions.drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=results_pose.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS)
            cv2.imshow('MediaPipe Pose', frame) 

            results_face = face_mesh.process(frame_rgb)
            if results_face.multi_face_landmarks:
                for face_landmarks in results_face.multi_face_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                        connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1),
                    )
                cv2.imshow('Face Estimation', frame)

        # 結果を表示
        cv2.imshow("Skeleton Estimation", frame)

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
