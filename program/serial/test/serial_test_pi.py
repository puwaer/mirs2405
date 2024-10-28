import serial
import struct
import time

def setup_serial(port='/dev/ttyUSB0', baudrate=9600):
    """ シリアルポートを設定する関数 """
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # 接続の安定のため少し待つ
    return ser

def send_data(ser, number):
    """ データを送信する関数 """
    data = struct.pack('i', number)  # 整数をバイト列に変換
    ser.write(data)                   # シリアルポートを通してデータを送信
    print(f"Sent: {number}")          # 送信確認用メッセージ

def receive_data(ser):
    """ データを受信する関数 """
    if ser.in_waiting >= 4:  # 4バイト受信を確認
        data = ser.read(4)    # 4バイト読み込む
        number = struct.unpack('i', data)[0]  # バイト列を整数に変換
        print(f"Received: {number}")  # 受信したデータの表示

def main():
    ser = setup_serial()  # シリアルポートを設定
    try:
        while True:
            # データを受信
            receive_data(ser)
            # 送信する整数
            number = 5678  # 送信する整数
            send_data(ser, number)  # データを送信
            time.sleep(1)  # 1秒待つ
    except KeyboardInterrupt:
        ser.close()  # 終了時にシリアルポートを閉じる

if __name__ == "__main__":
    main()
