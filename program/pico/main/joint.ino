float target_ang_joint1;
float angle_joint1;

float err_ang_joint1;
float integral_ang_joint1;
float differential_ang_joint1;
float pre_err_ang_joint1;
int joint1_pwm;

float target_ang_joint2;
float angle_joint2;

float err_ang_joint2;
float integral_ang_joint2;
float differential_ang_joint2;
float pre_err_ang_joint2;
int joint2_pwm;

void joint1_initialize(float a, float *b){
  joint1_ang_limitter(a, &a);
  PID_reset_joint1();
  joint1_stop();

  *b = a;
}

void joint1_pwm_limitter(int a, int *b){
  if(a > joint1_pwm_limitter_H){
    *b = joint1_pwm_limitter_H;
  }
  else if(a < joint1_pwm_limitter_L){
    *b = joint1_pwm_limitter_L;
  }
  else if(0 < a && a < joint1_dead_zone){
    *b = joint1_dead_zone;
  }
  else if(-joint1_dead_zone < a && a < 0){
    *b = -joint1_dead_zone;
  }
  else{
    *b = a;
  }
}

void joint1_ang_limitter(float _ang, float *_return){
  if(joint1_ang_limitter_H <= _ang){
    *_return = joint1_ang_limitter_H;
  } 
  else if(_ang <= joint1_ang_limitter_L){
    *_return = joint1_ang_limitter_L;
  }
}

void PID_reset_joint1(){
  err_ang_joint1 = 0.0;
  integral_ang_joint1 = 0.0;
  differential_ang_joint1 = 0.0;
  pre_err_ang_joint1 = 0.0;
  joint1_pwm = 0.0;
}

void PID_joint1(float a, float b, int *c){
  err_ang_joint1 = a - b;
  integral_ang_joint1 += (err_ang_joint1 + pre_err_ang_joint1) * (control_period / 2000.0);
  differential_ang_joint1 = (err_ang_joint1 - pre_err_ang_joint1) / (control_period / 1000.0);
  joint1_pwm = Kp_joint1 * err_ang_joint1 + Ki_joint1 * integral_ang_joint1 + Kd_joint1 * differential_ang_joint1;
  *c = (int)(joint1_pwm + 0.5);
  pre_err_ang_joint1 = err_ang_joint1;
}

void joint1(float _angle) {
  joint1_initialize(_angle, &target_ang_joint1);
  while(1){
    angle_joint1 = analogRead(PIN_JOINT_1_POT);
    angle_joint1 = map(angle_joint1, 0, 1023, POT_MIN, POT_MAX);
    PID_joint1(target_ang_joint1, angle_joint1, &joint1_pwm);
    joint1_pwm_limitter(joint1_pwm, &joint1_pwm);

    if(abs(target_ang_joint1) < abs(angle_joint1)){
      joint1_stop();
      break;
    }
    if(target_ang_joint1 == 0){
      joint1_stop();
      break;
    }

    joint1_R_run(joint1_pwm);
    joint1_L_run(-joint1_pwm);

    delay(10);
  } 
}

void joint1_stop(){
  analogWrite(PIN_JOINT_1_R_PWM, 0);
  analogWrite(PIN_JOINT_1_R_PWM, 0);
}

void joint1_R_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_R_DIR, HIGH);
    analogWrite(PIN_JOINT_1_R_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_R_DIR, LOW);
    analogWrite(PIN_JOINT_1_R_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_1_R_PWM, 0);
  }
}

void joint1_L_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_L_DIR, HIGH);
    analogWrite(PIN_JOINT_1_L_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_1_L_DIR, LOW);
    analogWrite(PIN_JOINT_1_L_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_1_L_PWM, 0);
  }
}

void joint2_initialize(float a, float *b){
  joint2_ang_limitter(a, &a);
  PID_reset_joint2();
  joint2_stop();

  *b = a;
}

void joint2_pwm_limitter(int a, int *b){
  if(a > joint2_pwm_limitter_H){
    *b = joint2_pwm_limitter_H;
  }
  else if(a < joint2_pwm_limitter_L){
    *b = joint2_pwm_limitter_L;
  }
  else if(0 < a && a < joint2_dead_zone){
    *b = joint2_dead_zone;
  }
  else if(-joint2_dead_zone < a && a < 0){
    *b = -joint2_dead_zone;
  }
  else{
    *b = a;
  }
}

void joint2_ang_limitter(float _ang, float *_return){
  if(joint2_ang_limitter_H <= _ang){
    *_return = joint1_ang_limitter_H;
  } 
  else if(_ang <= joint2_ang_limitter_L){
    *_return = joint1_ang_limitter_L;
  }
}

void PID_reset_joint2(){
  err_ang_joint2 = 0.0;
  integral_ang_joint2 = 0.0;
  differential_ang_joint2 = 0.0;
  pre_err_ang_joint2 = 0.0;
  joint2_pwm = 0.0;
}

void PID_joint2(float a, float b, int *c){
  err_ang_joint2 = a - b;
  integral_ang_joint2 += (err_ang_joint2 + pre_err_ang_joint2) * (control_period / 2000.0);
  differential_ang_joint2 = (err_ang_joint2 - pre_err_ang_joint2) / (control_period / 1000.0);
  joint2_pwm = Kp_joint2 * err_ang_joint2 + Ki_joint2 * integral_ang_joint2 + Kd_joint2 * differential_ang_joint2;
  *c = (int)(joint2_pwm + 0.5);
  pre_err_ang_joint2 = err_ang_joint2;
}

void joint2(float _angle) {
  joint2_initialize(_angle, &target_ang_joint2);
  while(1){
    angle_joint2 = analogRead(PIN_JOINT_2_POT);
    angle_joint2 = map(angle_joint2, 0, 1023, POT_MIN, POT_MAX);
    PID_joint2(target_ang_joint2, angle_joint2, &joint2_pwm);
    joint2_pwm_limitter(joint2_pwm, &joint2_pwm);

    if(abs(target_ang_joint2) < abs(angle_joint2)){
      joint2_stop();
      break;
    }
    if(target_ang_joint2 == 0){
      joint2_stop();
      break;
    }

    joint2_run(joint2_pwm);
    delay(10);
  } 
}

void joint2_stop(){
  analogWrite(PIN_JOINT_2_PWM, 0);
}

void joint2_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_2_DIR, HIGH);
    analogWrite(PIN_JOINT_2_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_2_DIR, LOW);
    analogWrite(PIN_JOINT_2_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_2_PWM, 0);
  }
}

void joint3(byte _id, int _ang, int _vel) {
  joint3_ang_limitter(_ang, &_ang);
  _ang = map(_ang, 0, 300, 0, 1023);
  _vel = map(_vel, 0, SCS_MAX_VEL, 0, 200);

  // コマンドパケットを作成
  byte message[13];
  message[0] = 0xFF;  // ヘッダ
  message[1] = 0xFF;  // ヘッダ
  message[2] = _id;   // サーボID
  message[3] = 9;     // パケットデータ長
  message[4] = 3;     // コマンド（3は書き込み命令）
  message[5] = 42;    // レジスタ先頭番号
  message[6] = (_ang >> 8) & 0xFF; // 位置情報バイト上位
  message[7] = _ang & 0xFF;  // 位置情報バイト下位
  message[8] = 0x00;  // 時間情報バイト下位
  message[9] = 0x00;  // 時間情報バイト上位
  message[10] = (_vel >> 8) & 0xFF; // 速度情報バイト上位
  message[11] = _vel & 0xFF; // 速度情報バイト下位

  // チェックサムの計算
  byte checksum = 0;
  for (int i = 2; i < 12; i++) {
    checksum += message[i];
  }
  message[12] = ~checksum; // チェックサム

  // コマンドパケットを送信
  for (int i = 0; i < 13; i++) {
    Serial1.write(message[i]);
  }
}

void joint3_ang_limitter(int _ang, int *_return){
  if(joint3_ang_limitter_H <= _ang){
    *_return = joint3_ang_limitter_H;
  } 
  else if(_ang <= joint3_ang_limitter_L){
    *_return = joint3_ang_limitter_L;
  }
}

void joint4(byte _id, int _ang, int _vel) {
  joint4_ang_limitter(_ang, &_ang);
  _ang = map(_ang, 0, 300, 0, 1023);
  _vel = map(_vel, 0, SCS_MAX_VEL, 0, 200);

  // コマンドパケットを作成
  byte message[13];
  message[0] = 0xFF;  // ヘッダ
  message[1] = 0xFF;  // ヘッダ
  message[2] = _id;   // サーボID
  message[3] = 9;     // パケットデータ長
  message[4] = 3;     // コマンド（3は書き込み命令）
  message[5] = 42;    // レジスタ先頭番号
  message[6] = (_ang >> 8) & 0xFF; // 位置情報バイト上位
  message[7] = _ang & 0xFF;  // 位置情報バイト下位
  message[8] = 0x00;  // 時間情報バイト下位
  message[9] = 0x00;  // 時間情報バイト上位
  message[10] = (_vel >> 8) & 0xFF; // 速度情報バイト上位
  message[11] = _vel & 0xFF; // 速度情報バイト下位

  // チェックサムの計算
  byte checksum = 0;
  for (int i = 2; i < 12; i++) {
    checksum += message[i];
  }
  message[12] = ~checksum; // チェックサム

  // コマンドパケットを送信
  for (int i = 0; i < 13; i++) {
    Serial2.write(message[i]);
  }
}

void joint4_ang_limitter(int _ang, int *_return){
  if(joint4_ang_limitter_H <= _ang){
    *_return = joint4_ang_limitter_H;
  } 
  else if(_ang <= joint4_ang_limitter_L){
    *_return = joint4_ang_limitter_L;
  }
}

