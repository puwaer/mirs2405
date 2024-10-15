static long cnt_l        = 0;
static long cnt_r        = 0;
static int  l_show_count = 0;
static int  r_show_count = 0;

void encoder_get(float *a, float *b){
  *a = cnt_l * run_PP;
  *b = cnt_r * run_PP;
}

void encoder_reset(){
  cnt_l = 0;
  cnt_r = 0;
}

void enc_change_l() {
  l_show_count++;
  if(l_show_count>100){
    //show_l();
    l_show_count=0;
  }
  int a_curr;
  int b_curr;
  static int a_prev = LOW;
  static int b_prev = LOW;
  a_curr = digitalRead(PIN_ENC_A_L);
  b_curr = digitalRead(PIN_ENC_B_L);
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) cnt_l--;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) cnt_l--;
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) cnt_l++;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) cnt_l++;
  a_prev = a_curr;
  b_prev = b_curr;
}

void enc_change_r() {
  r_show_count++;
  if(r_show_count>200){
    //show_r();
    r_show_count=0;
  }
  int a_curr;
  int b_curr;
  static int a_prev = LOW;
  static int b_prev = LOW;
  a_curr = digitalRead(PIN_ENC_A_R);
  b_curr = digitalRead(PIN_ENC_B_R);
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW) cnt_r++;
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH) cnt_r++;
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH) cnt_r--;
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW) cnt_r--;
  a_prev = a_curr;
  b_prev = b_curr;
}

void show_l(){
  Serial.print("Left: ");
  Serial.println(cnt_l);
}

void show_r(){
  Serial.print("Right: ");
  Serial.println(cnt_r);
}
