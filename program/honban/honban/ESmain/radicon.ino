const int SEND_ARRAY_SIZE = 7;
//const int SEND_ARRAY_SIZE = 9;
unsigned int sendArray[SEND_ARRAY_SIZE]; //送信する配列を格納

static int var = 0;
static int old_var = 0; 
int state = 0;
int maxState = 2;


void send_rc(){
  // 各ピンからパルス幅を取得
  while(1){
    sendArray[0] = 4;
    sendArray[1] = pulseIn(PIN_MR8_A, HIGH);
    sendArray[2] = pulseIn(PIN_MR8_B, HIGH);
    sendArray[3] = pulseIn(PIN_MR8_C, HIGH);
    sendArray[4] = pulseIn(PIN_MR8_D, HIGH);
    sendArray[5] = pulseIn(PIN_MR8_G, HIGH);
    sendArray[6] = pulseIn(PIN_MR8_F, HIGH);

      // 各int型データを2バイトに分けて送信
    for (int i = 0; i < SEND_ARRAY_SIZE ; i++) {
      Serial.write(sendArray[i] & 0xFF);         // 下位バイト
      Serial.write((sendArray[i] >> 8) & 0xFF);  // 上位バイト
    }

    delay(10); // 送信間隔
  }
}
