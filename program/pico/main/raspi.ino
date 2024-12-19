const int RECEIVE_ARRAY_SIZE = 5;  // 受信する配列の要素数
uint16_t receivedArray[RECEIVE_ARRAY_SIZE]; // 受信した配列を格納
int old_receivedArray[RECEIVE_ARRAY_SIZE];

const int SEND_ARRAY_SIZE = 5;
unsigned int sendArray[SEND_ARRAY_SIZE]; //送信する配列を格納

void raspi_receive(){
  static int receivedIndex = 0;
  uint8_t highByte, lowByte;

  /*for(int i = 0; i < RECEIVE_ARRAY_SIZE; i++){
    old_receivedArray[i] = receivedArray[i];
    Serial.print(receivedArray[i]);
  }
  Serial.println();*/

  if (Serial.available() >= 2) {  // 2バイト受信可能か確認
    highByte = Serial.read();     // 上位バイトを読み取る
    lowByte = Serial.read();      // 下位バイトを読み取る

    // 特別な終了シンボル (0xFFFF) のチェック
    if(highByte == 0xFF && lowByte == 0xFF){
      // データを全て受信したら配列を表示
      Serial.println("Received data:");
      for (int i = 0; i < RECEIVE_ARRAY_SIZE; i++) {
        Serial.println(receivedArray[i]);
      }
      receivedIndex = 0;  // インデックスをリセット
    } 
    else {
      // 受信したデータを1つの整数に変換
      uint16_t value = (highByte << 8) | lowByte;
      if (receivedIndex < RECEIVE_ARRAY_SIZE) {
        receivedArray[receivedIndex++] = value;
      }
    }
  }

  bool arraysmatch = true;

  /*for (int i = 0; i < RECEIVE_ARRAY_SIZE; i++) {
    if (old_receivedArray[i] != receivedArray[i]) {
      arraysmatch = false; // 一致しない要素が見つかった場合
      break; // 比較を終了
    }
  }*/
  arraysmatch = false;

  if(receivedArray[0] == 4){
    radicon();
  }

  /*if(!arraysmatch){ //receivedArrayが変化した場合
    switch(receivedArray[0]){
    case -1:
      all_stop();
      break;
    
    case 0:
      break;

    case 1:
      raspi_send(0, 1, 0, 0, 0);
      break;

    case 2:
      run_To(receivedArray[1], receivedArray[2]);
      break; 

    case 3:
      arm(receivedArray[1], receivedArray[2], receivedArray[3], receivedArray[4]);
      break;
      
    case 4:
      radicon();
      break;

    case 5:
      photoreflector();
      break;

    default:
      break;
    }
  }*/
}

void raspi_send(int sendArray_0, int sendArray_1, int sendArray_2, int sendArray_3, int sendArray_4){
  sendArray[0] = sendArray_0;
  sendArray[1] = sendArray_1;
  sendArray[2] = sendArray_2;
  sendArray[3] = sendArray_3;
  sendArray[4] = sendArray_4;

  //Serial.write(0xFF);  // スタートバイトを送信
  for (int i = 0; i < SEND_ARRAY_SIZE; i++){
    Serial.write(sendArray[i] & 0xFF);         // 下位バイト
    Serial.write((sendArray[i] >> 8) & 0xFF);  // 上位バイト
  }
  //Serial.write(0xFE); 
}

