void arm(float _ang1, float _ang2, float _ang3, float _ang4){
  joint3_4(joint4ID, _ang4);
  joint3_4(joint3ID, _ang3); 
  joint2(_ang2);
  joint1(_ang1);

}
