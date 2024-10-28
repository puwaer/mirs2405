void setup() {
  Serial.begin(9600); // ボーレートを9600に設定
}

void loop() {
  // 受信データの処理
  receiveData(); // データを受信
  
  // 送信する整数
  int number = 1234; 
  sendData(number);  // データを送信
  delay(1000);       // 1秒待つ
}

// データを送信する関数
void sendData(int number) {
  Serial.write((byte *)&number, sizeof(number)); // 整数を送信
  Serial.println("Data sent!"); // デバッグ用メッセージ
}

// データを受信する関数
void receiveData() {
  if (Serial.available() >= 4) {  // 4バイト受信を確認
    int32_t number;
    Serial.readBytes((byte *)&number, sizeof(number)); // 受信データを読み込む
    Serial.print("Received: ");
    Serial.println(number); // 受信したデータの表示
  }
}
