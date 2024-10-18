
void arm(float _ang1, float _ang3, float _ang4){
  scs_2.write(_ang4);  //動くかわからない
  scs_1.write(_ang3);  //動くかわからない
  

}

void pot_change(){
  int a_curr;
  int a_prev;
  a_curr = analogRead(PIN_JOINT_1_POT);

  a_prev = a_curr;
}

/*
シリアルサーボの制御方法
第一関節同時に動かす方法
ポテンショメータはどのモータ

*/