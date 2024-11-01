int dataArray[] = {10, 20, 30, 40, 50};
int dataSize = sizeof(dataArray) / sizeof(dataArray[0]);

void setup() {
  Serial.begin(9600);  // ボーレートを設定
}

void loop() {
  // データサイズを送信（配列の長さ）
  Serial.write(dataSize);
  
  // 配列データを順に送信
  for (int i = 0; i < dataSize; i++) {
    Serial.write(dataArray[i]);
  }

  delay(1000);  // データ送信間隔
}
