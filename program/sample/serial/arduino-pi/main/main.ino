const int size = 5; // 配列のサイズ
unsigned int inputValues[size] = {1, 2, 2, 3, 4}; // 入力値を格納する配列

void setup() {
  Serial.begin(9600); // シリアル通信を初期化
}

void send_data() {
  Serial.write(0xFF); // スタートバイトを送信

  // 各unsigned int型データを2バイトに分けて送信
  for (int i = 0; i < size; i++) {
    Serial.write(inputValues[i] & 0xFF);         // 下位バイト
    Serial.write((inputValues[i] >> 8) & 0xFF);  // 上位バイト
  }

  Serial.write(0xFE); // エンドバイトを送信

  delay(100); // 送信間隔（100msごとに送信）
}

void loop() {
  send_data();
}