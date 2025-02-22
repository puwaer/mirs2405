const int RECEIVE_ARRAY_SIZE = 7;  // 受信する配列の要素数
uint16_t receivedArray[RECEIVE_ARRAY_SIZE]; // 受信した配列を格納
int old_receivedArray[RECEIVE_ARRAY_SIZE];

const int SEND_ARRAY_SIZE = 7;
unsigned int sendArray[SEND_ARRAY_SIZE]; //送信する配列を格納

const int DATA_SIZE = 14; // 受信するデータのバイト数
int inputValues[DATA_SIZE / 2]={0, 0, 0, 0, 0, 0, 0}; // 2バイトで1つの値を格納

void raspi_receive() {
  inputValues[0]=0;
  // データが十分受信されているか確認
  if (Serial.available() >= DATA_SIZE) {
    delay(100);
    uint8_t receivedData[DATA_SIZE];

    // データを読み取り
    
    Serial.readBytes(receivedData, DATA_SIZE);
    while (Serial.available() > 0) {//受信バッファクリア
        char t = Serial.read();
     }
    // データを2バイトごとに組み合わせて整数値に変換
    for (int i = 0; i < DATA_SIZE; i += 2) {
      inputValues[i / 2] = (int16_t)(receivedData[i] | (receivedData[i + 1] << 8));
    }
    if(inputValues[0]==0){
      all_stop();
    }
    else if (inputValues[0]==1){
      raspi_send(0, 1, 0, 0, 0, 0, 0);
    }
    else if (inputValues[0]==2){
      run_To(inputValues[1], inputValues[2]);
    }
    else if (inputValues[0]==3){
      arm(inputValues[1], inputValues[2], inputValues[3], inputValues[4]);
      //inputValues[0]=0;
    }
    else if (inputValues[0]==4){
      radicon(inputValues[1], inputValues[2], inputValues[3], inputValues[4], inputValues[5], inputValues[6]);
    } 
    else if (inputValues[0]==5){    
      photoreflector();
    } 
    else if (inputValues[0]==6){
      get(inputValues[1], inputValues[2], inputValues[3], inputValues[4]);
    }
  
    //digitalWrite(13, LOW);
    //delay(100);

  } else {
    inputValues[0]=0;
  }
  while (Serial.available() > 0) {//受信バッファクリア
        char t = Serial.read();
  }
}

void raspi_send(int sendArray_0, int sendArray_1, int sendArray_2, int sendArray_3, int sendArray_4, int sendArray_5, int sendArray_6) {
  sendArray[0] = sendArray_0;
  sendArray[1] = sendArray_1;
  sendArray[2] = sendArray_2;
  sendArray[3] = sendArray_3;
  sendArray[4] = sendArray_4;
  sendArray[5] = sendArray_5;
  sendArray[6] = sendArray_6;
  for(int i = 0; i < DATA_SIZE/2 ; i++){
    Serial.write(sendArray[i] & 0xFF);
    Serial.write((sendArray[i] >> 8) & 0xFF);
  }
  delay(100);
}
