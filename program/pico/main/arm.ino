

void arm(float _ang1, float _ang2, float _ang3, float _ang4){
  joint4(joint4ID, _ang4, joint4_vel);
  joint3(joint3ID, _ang3, joint3_vel); 
  joint2(_ang2);
  joint1(_ang1);

}
