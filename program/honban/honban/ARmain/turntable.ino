static long cnt = 0;

float target_ang_turntable;
float angle_turntable;

float err_ang_turntable;
float integral_ang_turntable;
float differential_ang_turntable;
float pre_err_ang_turntable;
int turntable_pwm;

int turntable_count = 0;

void encoder_get(float *a){
  *a = cnt;
}

void encoder_reset(){
  cnt = 0;
}

void enc_change() {
  int a_curr;
  int b_curr;
  static int a_prev = LOW;
  static int b_prev = LOW;
  a_curr = digitalRead(PIN_TURNTABLEENC_A);
  b_curr = digitalRead(PIN_TURNTABLEENC_B);
  if (a_prev ==  LOW && b_prev == HIGH && a_curr == HIGH && b_curr ==  LOW){
    cnt--;
  } 
  if (a_prev == HIGH && b_prev ==  LOW && a_curr ==  LOW && b_curr == HIGH){
    cnt--;
  }
  if (a_prev ==  LOW && b_prev ==  LOW && a_curr == HIGH && b_curr == HIGH){
    cnt++;
  }  
  if (a_prev == HIGH && b_prev == HIGH && a_curr ==  LOW && b_curr ==  LOW){
    cnt++;
  } 
  a_prev = a_curr;
  b_prev = b_curr;
}

void turntable_initialize(float a, float *b){
  encoder_reset();
  PID_reset_turntable();
  turntable_stop();

  *b = map(a, -180, 180, -turntable_PPR/2, turntable_PPR/2);
}

void turntable_limitter(int a, int *b){
  if(a > turntable_pwm_limitter_H){
    *b = turntable_pwm_limitter_H;
  }
  else if(a < turntable_pwm_limitter_L){
    *b = turntable_pwm_limitter_L;
  }
  else if(0 < a && a < turntable_dead_zone){
    *b = turntable_dead_zone;
  }
  else if(-turntable_dead_zone < a && a < 0){
    *b = -turntable_dead_zone;
  }
  else{
    *b = a;
  }
}

void PID_reset_turntable(){
  err_ang_turntable = 0.0;
  integral_ang_turntable = 0.0;
  differential_ang_turntable = 0.0;
  pre_err_ang_turntable = 0.0;
  turntable_pwm = 0.0;
}

void PID_turntable(float a, float b, int *c){
  err_ang_turntable = a - b;
  integral_ang_turntable += (err_ang_turntable + pre_err_ang_turntable) * (control_period / 2000.0);
  differential_ang_turntable = (err_ang_turntable - pre_err_ang_turntable) / (control_period / 1000.0);
  turntable_pwm = Kp_turntable * err_ang_turntable + Ki_turntable * integral_ang_turntable + Kd_turntable * differential_ang_turntable;
  *c = (int)(turntable_pwm + 0.5);
  pre_err_ang_turntable = err_ang_turntable;
}

void turntable(float _angle) {
  turntable_initialize(_angle, &target_ang_turntable);
  turntable_count = 0;
  while(1){
    if(turntable_count > 1000){
      turntable_count = 0;
      break;
    }
    turntable_count++;
    encoder_get(&angle_turntable);
    PID_turntable(target_ang_turntable, angle_turntable, &turntable_pwm);
    turntable_limitter(turntable_pwm, &turntable_pwm);

    if(abs(target_ang_turntable) < abs(angle_turntable)){
      turntable_stop();
      break;
    }
    if(target_ang_turntable == 0){
      turntable_stop();
      break;
    }
    
    turntable_pwm = -turntable_pwm;

    int LS_K_state = digitalRead(PIN_LS_K);
    if(LS_K_state == 0){
        PUMP_run(0);
    }
    
    Serial.print("angle_turntable = ");
    Serial.print(angle_turntable);
    Serial.print(",  target_ang_turntable = ");
    Serial.print(target_ang_turntable);
    Serial.print(",  turntable_pwm = ");
    Serial.print(turntable_pwm);
    Serial.println();
    

    turntable_run(turntable_pwm);
    delay(10);
  } 
}

void turntable_stop(){
  analogWrite(PIN_TURNTABLE_PWM, 0);
}

void turntable_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_TURNTABLE_DIR, HIGH);
    analogWrite(PIN_TURNTABLE_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_TURNTABLE_DIR, LOW);
    analogWrite(PIN_TURNTABLE_PWM, _pwm);
  }
  else{
    analogWrite(PIN_TURNTABLE_PWM, 0);
  }
}
