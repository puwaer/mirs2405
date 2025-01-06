void arm_init(){
  pinMode(PIN_GRIPPER_PWM, OUTPUT);
  pinMode(PIN_AIRCHUCK_1_PWM, OUTPUT);
  pinMode(PIN_AIRCHUCK_2_PWM, OUTPUT);
  grip.attach(PIN_GRIPPER_PWM, GRIP_MAX, GRIP_MIN);
  airchuck1.attach(PIN_AIRCHUCK_1_PWM, AIRCHUCK_MIN, AIRCHUCK_MAX);
  airchuck2.attach(PIN_AIRCHUCK_2_PWM, AIRCHUCK_MIN, AIRCHUCK_MAX);

  grip.write(GRIP_OPEN_ANG);
  airchuck1.write(0);
  airchuck2.write(0);

  pinMode(PIN_PUMP_PWM, OUTPUT);
  pinMode(PIN_PUMP_DIR, OUTPUT);
  digitalWrite(PIN_PUMP_DIR, HIGH);

}

void turntable_init(){
  pinMode(PIN_TURNTABLE_PWM, OUTPUT);
  pinMode(PIN_TURNTABLE_DIR, OUTPUT);
  pinMode(PIN_TURNTABLEENC_A, INPUT);
  pinMode(PIN_TURNTABLEENC_B, INPUT);
  digitalWrite(PIN_TURNTABLE_DIR, HIGH);
  digitalWrite(PIN_TURNTABLEENC_A, HIGH);
  digitalWrite(PIN_TURNTABLEENC_B, HIGH);
  attachInterrupt(digitalPinToInterrupt(PIN_TURNTABLEENC_A), enc_change, CHANGE);
}

void raspi_open(){
  while(!Serial.available()){
    Serial.read();
    Serial.println("Raspberry Pi No signal");
    Serial.println("Press any key to skip");
    delay(1000);
  }
}
