void set_pin(){
  // FS90 のピン宣言
  pinMode(PIN_FS90_1_PWM, OUTPUT);
  pinMode(PIN_FS90_2_PWM, OUTPUT);
  pinMode(PIN_FS90_3_PWM, OUTPUT);

  // JC-578VA のピン宣言
  pinMode(PIN_JC578VA_1_PWM, OUTPUT);
  pinMode(PIN_JC578VA_2_PWM, OUTPUT);
  pinMode(PIN_JC578VA_1_DIR, OUTPUT);
  pinMode(PIN_JC578VA_2_DIR, OUTPUT);

  // LC-578VA のピン宣言
  pinMode(PIN_LC578VA_PWM, OUTPUT);
  pinMode(PIN_LC578VA_DIR, OUTPUT);

  // KS5N-IG36P のピン宣言
  pinMode(PIN_KS5NIG36P_PWM, OUTPUT);
  pinMode(PIN_KS5NIG36P_DIR, OUTPUT);

  // RS540 のピン宣言
  pinMode(PIN_RS540_PWM, OUTPUT);
  pinMode(PIN_RS540_DIR, OUTPUT);

  // FS5115M のピン宣言
  pinMode(PIN_FS5115M_1_PWM, OUTPUT);
  pinMode(PIN_FS5115M_2_PWM, OUTPUT);
  
  // 赤外線LED のピン宣言
  pinMode(PIN_INFRARED_LED, OUTPUT); 

  // ポテンショメータ のピン宣言
  pinMode(PIN_POTENTIOMETER_1, INPUT); 
  pinMode(PIN_POTENTIOMETER_2, INPUT); 

  // フォトリフレクタ のピン宣言
  pinMode(PIN_PHOTOREFLECTOR, INPUT); 
}
