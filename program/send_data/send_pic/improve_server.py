import socketserver
import cv2
import sys

HOST = "172.25.16.100"  
PORT = 5569


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            ret, frame = videoCap.read()
            if not ret:
                break
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            _, jpegs_byte = cv2.imencode('.jpeg', frame, encode_param)
            data = jpegs_byte.tobytes()
            size = len(data).to_bytes(4, byteorder='big')
            self.request.sendall(size + data)

videoCap = cv2.VideoCapture(0)
socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer((HOST, PORT), TCPHandler)


try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit()
