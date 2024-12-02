const int inputPins[6] = {3, 5, 6, 9, 10, 11}; // ラジコン入力のピン
unsigned int inputValues[6]; // 入力値を格納する配列

void setup() {
  Serial.begin(9600); // シリアル通信を初期化
  for (int i = 0; i < 6; i++) {
    pinMode(inputPins[i], INPUT); // ピンを入力モードに設定
  }
}

void loop() {
  // 各ピンからパルス幅を取得
  for (int i = 0; i < 6; i++) {
    inputValues[i] = pulseIn(inputPins[i], HIGH); // 必要に応じてスケーリング
  }
  
  // 各int型データを2バイトに分けて送信
  for (int i = 0; i < 6; i++) {
    Serial.write(inputValues[i] & 0xFF);         // 下位バイト
    Serial.write((inputValues[i] >> 8) & 0xFF);  // 上位バイト
  }

  delay(100); // 送信間隔
}
