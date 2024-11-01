void receive(){
  int a = pulseIn(MR8_A_PIN, HIGH);
  /*int b = pulseIn(MR8_B_PIN, HIGH);
  int c = pulseIn(MR8_C_PIN, HIGH);
  int d = pulseIn(MR8_D_PIN, HIGH);
  int e = pulseIn(MR8_E_PIN, HIGH);
  int f = pulseIn(MR8_F_PIN, HIGH);
  int g = pulseIn(MR8_G_PIN, HIGH);
  int h = pulseIn(MR8_H_PIN, HIGH);*/

  Serial.print("A=");
  Serial.println(a);
  /*Serial.print(" B=");
  Serial.print(b);
  Serial.print(" C=");
  Serial.print(c);
  Serial.print(" D=");
  Serial.print(d);
  Serial.print(" E=");
  Serial.print(e);
  Serial.print(" F=");
  Serial.print(f);
  Serial.print(" G=");
  Serial.print(g);
  Serial.print(" H=");
  Serial.println(h);*/
  delay(100);
}