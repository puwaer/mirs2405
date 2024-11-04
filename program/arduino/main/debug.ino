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
