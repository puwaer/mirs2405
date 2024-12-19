import serial
import time
import send

#jetson
#def receive_position():



#pico

def receive_and_forward_rc(receive_port='/dev/ttyACM0', forward_port='/dev/ttyACM0', baudrate=115200):
    """
    シリアルポートでデータを受信し、他のポートにそのまま転送する関数。
    """
    # シリアル通信の初期化
    ser_receive = serial.Serial(receive_port, baudrate)
    ser_forward = serial.Serial(forward_port, baudrate)
    time.sleep(2)  # シリアル通信の初期化待ち

    try:
        while True:
            # データが一定以上たまっている場合に受信
            if ser_receive.in_waiting >= 10:  # 10バイト以上のデータが待機中か確認
                data = ser_receive.read(10)  # 10バイトを一度に受信
                input_values = []

                # 2バイトごとに組み合わせてintに変換
                for i in range(0, len(data), 2):  # len(data)を使って、データ長に依存する
                    pulse_value = data[i] | (data[i + 1] << 8)
                    input_values.append(pulse_value)
                
                # 転送データをそのまま送信
                ser_forward.write(data)

                print("Received input values:", input_values)
                
                # 特定の条件が満たされたらループを終了
                if len(input_values) > 4 and input_values[4] == 1:  # input_valuesの長さをチェック
                    print("Terminating based on received signal.")
                    break

    except serial.SerialException as e:
        # シリアル通信エラーの処理
        print(f"Serial communication error: {e}")
    except Exception as e:
        # その他のエラーの処理
        print(f"An unexpected error occurred: {e}")
    finally:
        # シリアルポートを閉じる
        ser_receive.close()
        ser_forward.close()

def receive_once():
    size = 5  # 配列のサイズ
    bytes_per_value = 2  # 各値は2バイト
    total_bytes = size * bytes_per_value

    ser = serial.Serial('/dev/ttyACM0', 115200)
    time.sleep(2)  # シリアル通信の初期化待ち

    input_values = []  # 受信したデータを格納するリスト

    while True:
        # データが十分に待機しているか確認
        if ser.in_waiting >= total_bytes:
            data = ser.read(total_bytes)  # 配列データを取得

            # データを2バイトずつ整数に変換
            for i in range(0, total_bytes, 2):
                pulse_value = data[i] | (data[i + 1] << 8)
                input_values.append(pulse_value)

            print("Received input values:", input_values)
            break  # 受信後はループを抜ける

        # データがまだ受信されていない場合は、ループを続ける
        print("Waiting for data...")

    ser.close()  # シリアルポートを閉じる
    return input_values  # 受信したデータを返す


#arduino





