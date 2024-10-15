
void arm(float _ang1, float _ang3, float _ang4){
  scs_2.write(ang4);  //動くかわからない
  scs_1.write(ang3);  //動くかわからない
  

}

potent_change_l(){
  int a_curr;
  int a_prev;
  a_curr = analogRead(PIN_POTENTIOMETER_L);

  a_prev = a_curr;
}

potent_change_r(){

}

/*
シリアルサーボの制御方法
第一関節同時に動かす方法
ポテンショメータはどのモータ

*/