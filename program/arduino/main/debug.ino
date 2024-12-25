void turntable_debug(){
  int _ang = 30;
  turntable(_ang);
}

void grip_debug(){
  while(1){
    airchuck(false);
    delay(2000);
    airchuck(true);
    delay(2000);
  }
}
