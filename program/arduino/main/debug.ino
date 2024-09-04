
void run_debug(){
  x_coordinate = 10;
  y_coordinate = 10;
  run_ToPerson(x_coordinate, y_coordinate);
  if((T >= T_GIVE) || (hand_check() == 0)){
    timer(0);
    state = REFILL;
  }
}

void show_XXX(){
  
}
