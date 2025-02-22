void gripper(bool _check){
  if(_check == true){
    grip.write(GRIP_OPEN_ANG);
  }
  else if(_check == false){
    grip.write(GRIP_CLOSE_ANG);
  }
}

void airchuck(bool _check){
  if(_check == false){
    airchuck1.write(AIRCHUCK_ANG);
    airchuck2.write(AIRCHUCK_ANG);
  }
  else if(_check == true){
    airchuck1.write(0);
    airchuck2.write(0);
  }
}

void PUMP(bool _check){
  if(_check == false){
    PUMP_run(pump_pwm);
    delay(pump_time);
    PUMP_run(0);
  }
  else if(_check == true){
    PUMP_run(-pump_pwm);
    delay(pump_time);
    PUMP_run(0);
  }
}

void PUMP_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_PUMP_DIR, HIGH);
    analogWrite(PIN_PUMP_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_PUMP_DIR, LOW);
    analogWrite(PIN_PUMP_PWM, _pwm);
  }
  else{
    analogWrite(PIN_PUMP_PWM, 0);
  }
}

void ultrasonic(){
  int reading;
  Wire.beginTransmission(112);
  Wire.write(byte(0x00));
  Wire.write(byte(0x51));
  Wire.endTransmission();

  delay(70);

  Wire.beginTransmission(112);
  Wire.write(byte(0x02));
  Wire.endTransmission();

  Wire.requestFrom(112, 2);

  if (2 <= Wire.available()){
    reading = Wire.read();
    reading = reading << 8;
    reading |= Wire.read();
    Serial.print(reading);
    Serial.println("cm");
  }
  delay(30);

  //raspi_send(10, reading, 0, 0, 0);

}