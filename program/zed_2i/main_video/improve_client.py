import socket
import numpy
import cv2


HOST = '172.25.15.27'
PORT = 5700

def getimage(sock):
    size = int.from_bytes(sock.recv(4), byteorder='big')
    buf = b''
    while len(buf) < size:
        buf += sock.recv(size - len(buf))
    recdata = numpy.frombuffer(buf, dtype='uint8')
    return cv2.imdecode(recdata, 1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    img = getimage(sock)
    cv2.imshow('Capture', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

sock.close()
cv2.destroyAllWindows()
