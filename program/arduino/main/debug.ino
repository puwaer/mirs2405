void turntable_debug(){
  int _ang = 30;
  while(1){
    turntable(_ang);
    delay(2000);
    turntable(-_ang);
    delay(2000);
  }
  
}

void grip_debug(){
  while(1){
    airchuck(false);
    delay(2000);
    airchuck(true);
    delay(2000);
  }
}
