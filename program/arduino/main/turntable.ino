float target_ang_turntable;
float angle_turntable;

float err_ang_turntable;
float integral_ang_turntable;
float differential_ang_turntable;
float pre_err_ang_turntable;
int turntable_pwm;

void turntable_initialize(float a, float *b){
  encoder_reset();
  PID_reset_turntable();
  turntable_stop();

  *b = a;
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
  while(1){
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
