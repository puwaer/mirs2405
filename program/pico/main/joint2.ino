float target_ang_joint2;
float angle_joint2;

float err_ang_joint2;
float integral_ang_joint2;
float differential_ang_joint2;
float pre_err_ang_joint2;
int joint2_pwm;

void joint2_initialize(float a, float *b){
  PID_reset_joint2();
  joint2_stop();

  *b = a;
}

void joint2_limitter(int a, int *b){
  if(a > joint2_pwm_limitter_H){
    *b = joint2_pwm_limitter_H;
  }
  else if(a < joint2_pwm_limitter_L){
    *b = joint2_pwm_limitter_L;
  }
  else if(0 < a && a < joint2_dead_zone){
    *b = joint2_dead_zone;
  }
  else if(-joint2_dead_zone < a && a < 0){
    *b = -joint2_dead_zone;
  }
  else{
    *b = a;
  }
}

void PID_reset_joint2(){
  err_ang_joint2 = 0.0;
  integral_ang_joint2 = 0.0;
  differential_ang_joint2 = 0.0;
  pre_err_ang_joint2 = 0.0;
  joint2_pwm = 0.0;
}

void PID_joint2(float a, float b, int *c){
  err_ang_joint2 = a - b;
  integral_ang_joint2 += (err_ang_joint2 + pre_err_ang_joint2) * (control_period / 2000.0);
  differential_ang_joint2 = (err_ang_joint2 - pre_err_ang_joint2) / (control_period / 1000.0);
  joint2_pwm = Kp_joint2 * err_ang_joint2 + Ki_joint2 * integral_ang_joint2 + Kd_joint2 * differential_ang_joint2;
  *c = (int)(joint2_pwm + 0.5);
  pre_err_ang_joint2 = err_ang_joint2;
}

void joint2(float _angle) {
  joint2_initialize(_angle, &target_ang_joint2);
  while(1){
    angle_joint2 = analogRead(PIN_JOINT_2_POT);
    angle_joint2 = map(angle_joint2, 0, 1023, POT_MIN, POT_MAX);
    PID_joint2(target_ang_joint2, angle_joint2, &joint2_pwm);
    joint2_limitter(joint2_pwm, &joint2_pwm);

    if(abs(target_ang_joint2) < abs(angle_joint2)){
      joint2_stop();
      break;
    }
    if(target_ang_joint2 == 0){
      joint2_stop();
      break;
    }

    joint2_run(joint2_pwm);
    delay(10);
  } 
}

void joint2_stop(){
  analogWrite(PIN_JOINT_2_PWM, 0);
}

void joint2_run(int _pwm){
  if(_pwm > 0){
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_2_DIR, HIGH);
    analogWrite(PIN_JOINT_2_PWM, _pwm);
  }
  else if(_pwm < 0){
    _pwm = _pwm * -1;
    _pwm = _pwm;
    digitalWrite(PIN_JOINT_2_DIR, LOW);
    analogWrite(PIN_JOINT_2_PWM, _pwm);
  }
  else{
    analogWrite(PIN_JOINT_2_PWM, 0);
  }
}
