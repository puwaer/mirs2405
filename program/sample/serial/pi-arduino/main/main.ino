#include <Arduino.h>

int led = 2;
const int ARRAY_SIZE = 5;  // 受信する配列の要素数
uint16_t receivedArray[ARRAY_SIZE];  // 受信した配列を格納

void setup() {
  Serial.begin(115200);  // シリアル通信を初期化
  while (!Serial);     // シリアル接続が確立するまで待機
  Serial.println("Arduino ready to receive data.");
  pinMode(led, OUTPUT);
}

void loop() {

  digitalWrite(led, LOW);
  delay(100);

  static int index = 0;
  uint8_t highByte, lowByte;
  
  if (Serial.available() >= 2) {  // 2バイト受信可能か確認
    highByte = Serial.read();     // 上位バイトを読み取る
    lowByte = Serial.read();      // 下位バイトを読み取る

    // 特別な終了シンボル (0xFFFF) のチェック
    if (highByte == 0xFF && lowByte == 0xFF) {
      // データを全て受信したら配列を表示
      Serial.println("Received data:");
      for (int i = 0; i < ARRAY_SIZE; i++) {
        Serial.println(receivedArray[i]);
      }
      index = 0;  // インデックスをリセット
    } else {
      // 受信したデータを1つの整数に変換
      uint16_t value = (highByte << 8) | lowByte;
      if (index < ARRAY_SIZE) {
        receivedArray[index++] = value;
      }
    }
  }

  // 受信した配列の1番目の要素が0の場合にLEDを点灯
  if (receivedArray[1] == -30) {
    digitalWrite(led, HIGH);  // LEDを点灯
    delay(500);                // 500ミリ秒待機
    digitalWrite(led, LOW);   // LEDを消灯
    delay(500);                // 500ミリ秒待機
  }  
}
