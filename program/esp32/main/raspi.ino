const int RECEIVE_ARRAY_SIZE = 5;  // 受信する配列の要素数
uint16_t receivedArray[RECEIVE_ARRAY_SIZE]; // 受信した配列を格納

void raspi_receive(){
  static int index = 0;
  uint8_t highByte, lowByte;
 
  if (Serial.available() >= 2) {  // 2バイト受信可能か確認
    highByte = Serial.read();     // 上位バイトを読み取る
    lowByte = Serial.read();      // 下位バイトを読み取る

    // 特別な終了シンボル (0xFFFF) のチェック
    if (highByte == 0xFF && lowByte == 0xFF) {
      // データを全て受信したら配列を表示
      Serial.println("Received data:");
      for (int i = 0; i < RECEIVE_ARRAY_SIZE; i++) {
        Serial.println(receivedArray[i]);
      }
      index = 0;  // インデックスをリセット
    }
    else {
      // 受信したデータを1つの整数に変換
      uint16_t value = (highByte << 8) | lowByte;
      if (index < RECEIVE_ARRAY_SIZE) {
        receivedArray[index++] = value;
      }
    }
  }
  switch(receivedArray[0]){
  case 4:
    send_rc();
    break;
  }

}