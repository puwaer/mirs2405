void confirmation_device(){
  
}

void io_open(){
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BATT, INPUT);
  digitalWrite(PIN_LED, LOW);
}

void encoder_open(){
  pinMode(PIN_ENC_A_L, INPUT);
  pinMode(PIN_ENC_B_L, INPUT);
  pinMode(PIN_ENC_A_R, INPUT);
  pinMode(PIN_ENC_B_R, INPUT);
  digitalWrite(PIN_ENC_A_L, HIGH);
  digitalWrite(PIN_ENC_B_L, HIGH);
  digitalWrite(PIN_ENC_A_R, HIGH);
  digitalWrite(PIN_ENC_B_R, HIGH);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A_L), enc_change_l, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A_R), enc_change_r, CHANGE);
}

void motor_open(){
  pinMode(PIN_DIR_L, OUTPUT);
  pinMode(PIN_PWM_L, OUTPUT);
  pinMode(PIN_DIR_R, OUTPUT);
  pinMode(PIN_PWM_R, OUTPUT);
  motor_stop();
}

void raspi_open(){
  Serial.begin(115200);
  
  while(!Serial.available()){
    Serial.read();
    Serial.println("Raspberry Pi No signal");
    Serial.println("Press any key to skip");
    delay(1000);
  }
}

void arm_open(){
  pinMode(PIN_SCS215_1_PWM, OUTPUT);
  pinMode(PIN_SCS215_2_PWM, OUTPUT);
  scs_1.attach(PIN_SCS215_1_PWM);
  scs_2.attach(PIN_SCS215_2_PWM);

  pinMode(PIN_POTENTIOMETER_1, INPUT);
  pinMode(PIN_POTENTIOMETER_2, INPUT);

  pinMode(PIN_LC578VA_PWM, OUTPUT);
  pinMode(PIN_LC578VA_DIR, OUTPUT);

  pinMode(PIN_JC578VA_1_PWM, OUTPUT);
  pinMode(PIN_JC578VA_1_DIR, OUTPUT);

  pinMode(PIN_INFRARED_LED, OUTPUT);
  pinMode(PIN_PHOTOREFLECTOR, INPUT);

  attachInterrupt(digitalPinToInterrupt(POTENTIOMETER_R), potent_change_r, CHANGE);
  attachInterrupt(digitalPinToInterrupt(POTENTIOMETER_L), potent_change_l, CHANGE);
  
}

