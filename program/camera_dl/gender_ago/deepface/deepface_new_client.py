import socket
import numpy as np
import cv2
from deepface import DeepFace
import time
import threading
import queue

# サーバー接続設定
HOST = "172.25.18.20"  
PORT = 5569

# 最新の画像を管理するキュー
image_queue = queue.Queue(maxsize=1)

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

def age_analysis(image):
    """
    画像から年齢を推定する関数
    
    Args:
        image (numpy.ndarray): 分析する画像
    
    Returns:
        int or None: 推定された年齢
    """
    if image is None:
        return None
    
    try:
        result = DeepFace.analyze(image, actions=['age'], enforce_detection=False)
        return result[0]['age']
    except Exception as e:
        print("年齢推定エラー:", str(e))
        return None

def gender_analysis(image):
    """
    画像から性別を推定する関数
    
    Args:
        image (numpy.ndarray): 分析する画像
    
    Returns:
        str or None: 推定された性別
    """
    if image is None:
        return None
    
    try:
        result = DeepFace.analyze(image, actions=['gender'], enforce_detection=False)
        return result[0]['gender']
    except Exception as e:
        print("性別推定エラー:", str(e))
        return None

def main():
    """
    メインプログラム: ソケット接続、画像受信、分析を行う
    """
    # ソケット接続
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    print(f"接続先: {HOST}:{PORT}")
    print("画像受信中... 'q'キーで終了")
    
    # 画像受信用のスレッドを開始
    receiver_thread = threading.Thread(target=image_receiver_thread, args=(sock,), daemon=True)
    receiver_thread.start()
    
    try:
        while True:
            try:
                # キューから最新の画像を取得（待たない）
                img = image_queue.get_nowait()
                
                # 年齢推定
                estimated_age = age_analysis(img)
                if estimated_age is not None:
                    cv2.putText(img, f"Age: {estimated_age}", (10, 70), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print(estimated_age)

                # 性別推定
                estimated_gender = gender_analysis(img)
                if estimated_gender is not None:
                    cv2.putText(img, f"Gender: {estimated_gender}", (10, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print(estimated_gender)

                # 画像表示
                cv2.imshow('Face Analysis', img)
            
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