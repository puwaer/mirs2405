void pump_init(){
  pinMode(PIN_PUMP_PWM, OUTPUT);
  pinMode(PIN_PUMP_DIR, OUTPUT);
  digitalWrite(PIN_PUMP_DIR, HIGH);
  pinMode(PIN_LS_K, INPUT_PULLUP);
  pinMode(PIN_LS_H, INPUT_PULLUP);
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
  //attachInterrupt(digitalPinToInterrupt(PIN_TURNRABLEENC_B), enc_change, CHANGE);
}

void raspi_open(){
  while(!Serial.available()){
    Serial.read();
    Serial.println("Raspberry Pi No signal");
    Serial.println("Press any key to skip");
    delay(1000);
  }
}
