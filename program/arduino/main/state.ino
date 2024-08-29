void wait(){
  raspi_receive_person(&check);
  if(check == 1){
    timer(1);
    check = 0;
    state = GIVE;
  }
}

void give(){
  raspi_receive_coordinate(&x_coordinate, &y_coordinate, &arm_angle1, &arm_angle2, &arm_angle3, &arm_angle4, &arm_gripper);
  arm(&arm_angle1, &arm_angle2, &arm_angle3, &arm_angle4, &arm_gripper);
  run_ToPerson(x_coordinate, y_coordinate);

  if((T >= T_GIVE) || (hand_check() == 0)){
    timer(0);
    state = REFILL;
  }
}

void refill(){
  run_ToHome();
  if(hand_check() == 0){
    item_get();
  }
  state = WAIT;
}
