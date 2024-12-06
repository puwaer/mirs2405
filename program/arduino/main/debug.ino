void radicon_debug(){
  while(1){
    while(!Serial.available());
    String n = Serial.readString();   
    int A = n.toInt();
    while(!Serial.available());
    n = Serial.readString();   
    int C = n.toInt();
    while(!Serial.available());
    n = Serial.readString();   
    int F = n.toInt();
    
    radicon(A, C, F);
    
  }
  
}

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
