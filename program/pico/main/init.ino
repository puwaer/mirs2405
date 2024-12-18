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
    Serial.println(analogRead(PIN_JOINT_1_R_POT));
    Serial.read();
    Serial.println("Raspberry Pi No signal");
    Serial.println("Press any key to skip");
    delay(1000);
  }
}

void arm_open(){
  Serial1.setTX(PIN_JOINT_3_PWM);
  Serial2.setTX(PIN_JOINT_4_PWM);
  Serial1.begin(1000000);
  Serial2.begin(1000000);
  

  pinMode(PIN_JOINT_1_R_PWM, OUTPUT);
  pinMode(PIN_JOINT_1_L_PWM, OUTPUT);
  pinMode(PIN_JOINT_1_R_DIR, OUTPUT);
  pinMode(PIN_JOINT_1_L_DIR, OUTPUT);
  pinMode(PIN_JOINT_1_R_POT, INPUT);
  pinMode(PIN_JOINT_1_L_POT, INPUT);

  digitalWrite(PIN_JOINT_1_R_DIR, HIGH);
  digitalWrite(PIN_JOINT_1_L_DIR, HIGH);

  pinMode(PIN_JOINT_2_PWM, OUTPUT);
  pinMode(PIN_JOINT_2_DIR, OUTPUT);
  pinMode(PIN_JOINT_2_POT, INPUT);

  digitalWrite(PIN_JOINT_2_DIR, HIGH);

  pinMode(PIN_INFRARED_LED, OUTPUT);
  digitalWrite(PIN_INFRARED_LED, HIGH);
  pinMode(PIN_PHOTOREFLECTOR, INPUT);
  
}

void rc_init(){
  pinMode(PIN_MR8_A,INPUT);
  pinMode(PIN_MR8_C,INPUT);
  pinMode(PIN_MR8_E,INPUT);
  pinMode(PIN_MR8_F,INPUT);
}
