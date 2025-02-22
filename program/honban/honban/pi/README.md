# mirs2405 raspberry pi

・main.py：全体プログラム

・config.py：ポート、ボーレートを定義。ポートはたまに変わる。

・ポート確認
    arduino,pico：ls /dev/ttyACM*
    esp32       ：ls /dev/ttyUSB*
・ポートアクセス権限
    sudo chmod 666 /dev/ttyACM0

・inverse_kinematics.py：アーム角度計算

・receive.py：受信用プログラム
    serial_rc()：ラジコン通信用関数
    recive_pr()：フォトリフレクタ値の受信用関数

・send.py：送信用プログラム
    send_angle(data)：アーム角度送信用関数

・test.py：テスト用プログラム


