void receive(){
  a = pulseIn(MR8_A_PIN, HIGH);
  //b = pulseIn(MR8_B_PIN, HIGH);
  c = pulseIn(MR8_C_PIN, HIGH);
  //d = pulseIn(MR8_D_PIN, HIGH);
  e = pulseIn(MR8_E_PIN, HIGH);
  f = pulseIn(MR8_F_PIN, HIGH);
  g = pulseIn(MR8_G_PIN, HIGH);
  h = pulseIn(MR8_H_PIN, HIGH);

  Serial.print("A=");
  Serial.print(a);
  /*Serial.print(" B=");
  Serial.print(b);*/
  Serial.print(" C=");
  Serial.print(c);
  /*Serial.print(" D=");
  Serial.print(d);*/
  Serial.print(" E=");
  Serial.print(e);
  Serial.print(" F=");
  Serial.print(f);
  Serial.print(" G=");
  Serial.print(g);
  Serial.print(" H=");
  Serial.println(h);
  delay(100);
}