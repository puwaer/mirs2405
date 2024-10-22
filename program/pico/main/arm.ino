
void arm(float _ang1, float _ang2, float _ang3, float _ang4){
  scs_2.write(_ang4);  //動くかわからない
  scs_1.write(_ang3);  //動くかわからない
  joint2(_ang2);
  joint1(_ang1);
  
  

}

/*
シリアルサーボの制御方法
第一関節同時に動かす方法
ポテンショメータはどのモータ

*/