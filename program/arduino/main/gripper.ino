void gripper(bool _check){
  if(_check == false){
    grip.write(GRIP_ANG);
  }
  else if(_check == true){
    grip.write(0);
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

void PUMP(){
  
}
