void rc_init(){
  //pinMode(LED_PIN, OUTPUT);
  pinMode(MR8_A_PIN,INPUT);
  //pinMode(MR8_B_PIN,INPUT);
  pinMode(MR8_C_PIN,INPUT);
  //pinMode(MR8_D_PIN,INPUT);
  pinMode(MR8_E_PIN,INPUT);
  pinMode(MR8_F_PIN,INPUT);
  pinMode(MR8_G_PIN,INPUT);
  pinMode(MR8_H_PIN,INPUT);
  Serial.begin(115200);
  //delay(1000);
}