static long cnt = 0;

void encoder_get(float *a){
  *a = cnt * PPR;
}

void encoder_reset(){
  cnt = 0;
}

void enc_change() {
  int a_curr;
  int b_curr;
  static int a_prev = LOW;
  static int b_prev = LOW;
  a_curr = digitalRead(PIN_TURNTABLEENC_A);
  b_curr = digitalRead(PIN_TURNTABLEENC_B);
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) cnt--;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) cnt--;
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) cnt++;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) cnt++;
  a_prev = a_curr;
  b_prev = b_curr;
}