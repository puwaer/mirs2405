void PUMP(int _check){
  int LS_H_state = digitalRead(PIN_LS_H);
  int LS_K_state = digitalRead(PIN_LS_K);

  int count = 0;
  
  if(_check == 0){
    int p_pwm = 15;
    while(1){
      int LS_H_state = digitalRead(PIN_LS_H);
      int LS_K_state = digitalRead(PIN_LS_K);
  
      if(LS_H_state == 0){
        PUMP_run(0);
        break;
      }
  
      if(p_pwm >= PUMP_PWM_H_MAX){
        p_pwm = PUMP_PWM_H_MAX;
        long start = millis();
        if(millis() - start > 8500){
          p_pwm = 25;
        }
      }
      else{
        p_pwm += PUMP_PWM_H;
      }
      delay(30);
      PUMP_run(p_pwm);
    }
    
    PUMP_run(0);
  }
 

  if(_check == 1){
    int p_pwm = -15;
    while(1){
      count++;
      int LS_H_state = digitalRead(PIN_LS_H);
      int LS_K_state = digitalRead(PIN_LS_K);
      if(LS_K_state == 0){
        PUMP_run(0);
        break;
      }
      if(p_pwm <= PUMP_PWM_K_MAX){
        p_pwm = PUMP_PWM_K_MAX;
        long start = millis();
        if(millis() - start > 10000){
          p_pwm = -25;
        }
      }
      else{
        p_pwm -= PUMP_PWM_K;
      }
      delay(50);
      PUMP_run(p_pwm);
    }

    
  
    PUMP_run(0);
    p_pwm = 0;
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

  raspi_send(10, reading, 0, 0, 0, 0, 0);
}
