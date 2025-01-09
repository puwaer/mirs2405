const int RECEIVE_ARRAY_SIZE = 7;  // 受信する配列の要素数
uint16_t receivedArray[RECEIVE_ARRAY_SIZE]; // 受信した配列を格納
/*
void raspi_receive(){
  while(1){
    static int index = 0;
    uint8_t highByte, lowByte;
  
    if (Serial.available() >= 14) {  // 2バイト受信可能か確認
      for (int i = 0; i < RECEIVE_ARRAY_SIZE; i++) {
        highByte = Serial.read();     // 上位バイトを読み取る
        lowByte = Serial.read();      // 下位バイトを読み取る
        receivedArray[i]=(highByte << 8) | lowByte;
        //uint16_t value = (highByte << 8) | lowByte;  
        //receivedArray[index++] = value;
      }
    }

    if (receivedArray[0]==4){
      delay(1000);
      break;
    }

  }
}
*/
const int DATA_SIZE = 14; // 受信するデータのバイト数
int inputValues[DATA_SIZE / 2]; // 2バイトで1つの値を格納
void raspi_receive() {
  while(1){
    // データが十分受信されているか確認
    if (Serial.available() >= DATA_SIZE) {
      uint8_t receivedData[DATA_SIZE];

      // データを読み取り
      Serial.readBytes(receivedData, DATA_SIZE);

      // データを2バイトごとに組み合わせて整数値に変換
      for (int i = 0; i < DATA_SIZE; i += 2) {
        inputValues[i / 2] = receivedData[i] | (receivedData[i + 1] << 8);
      }

      if (inputValues[0]==4){
        delay(1000);
        break;
      }
    }
  }
}

