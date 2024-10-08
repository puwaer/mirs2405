void motor_stop(){
  analogWrite(PIN_PWM_L, 0);
  analogWrite(PIN_PWM_R, 0);
}

void motor_run_l(int pwm_l){
  if(pwm_l > 0){
    pwm_l = pwm_l;
    digitalWrite(PIN_DIR_L, LOW);
    analogWrite(PIN_PWM_L, pwm_l);
  }
  else if(pwm_l < 0){
    pwm_l = pwm_l * -1;
    pwm_l = pwm_l;
    digitalWrite(PIN_DIR_L, HIGH);
    analogWrite(PIN_PWM_L, pwm_l);
  }
  else{
    analogWrite(PIN_PWM_L, 0);
  }
}
void motor_run_r(int pwm_r){
  if(pwm_r > 0){
    digitalWrite(PIN_DIR_R, HIGH);
    analogWrite(PIN_PWM_R, pwm_r);
  }
  else if(pwm_r < 0){
    pwm_r = pwm_r * -1;
    digitalWrite(PIN_DIR_R, LOW);
    analogWrite(PIN_PWM_R, pwm_r);
  }
  else{
    analogWrite(PIN_PWM_R, 0);
  }
}
