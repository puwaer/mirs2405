import socketserver
import cv2
import sys
import time

HOST = "172.25.16.100"  # RaspberryPiのIPアドレスを入力
PORT = 5569
FRAME_RATE = 5  # 1秒間に5フレーム

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            start_time = time.time()
            
            ret, frame = videoCap.read()
            if not ret:
                break
            
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            _, jpegs_byte = cv2.imencode('.jpeg', frame, encode_param)
            data = jpegs_byte.tobytes()
            size = len(data).to_bytes(4, byteorder='big')
            self.request.sendall(size + data)
            
            # Calculate the time to wait to maintain the desired frame rate
            elapsed_time = time.time() - start_time
            wait_time = max(0, 1.0 / FRAME_RATE - elapsed_time)
            time.sleep(wait_time)

videoCap = cv2.VideoCapture(1)
socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer((HOST, PORT), TCPHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    videoCap.release()
    sys.exit()