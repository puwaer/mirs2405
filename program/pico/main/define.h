#define PIN_ENC_A_L   0
#define PIN_ENC_A_R   1
#define PIN_ENC_B_L   2  
#define PIN_ENC_B_R   3
#define PIN_DIR_R     4
#define PIN_DIR_L     5
#define PIN_PWM_R     6 
#define PIN_PWM_L     7

#define PIN_MR8_A   10
#define PIN_MR8_C   11
#define PIN_MR8_E   13
#define PIN_MR8_F   12

#define PIN_JOINT_1_L_PWM   14  //第一関節
#define PIN_JOINT_1_R_PWM   15
#define PIN_JOINT_1_L_DIR   18
#define PIN_JOINT_1_R_DIR   19
#define PIN_JOINT_1_L_POT   26 //26
#define PIN_JOINT_1_R_POT   27

#define PIN_JOINT_2_PWM   9  //第二関節9
#define PIN_JOINT_2_DIR   20  //20
#define PIN_JOINT_2_POT   28  //28

#define PIN_JOINT_3_PWM    16   //第三関節

#define PIN_JOINT_4_PWM    8   //第四関節

#define PIN_INFRARED_LED    21  //赤外線近接センサー
#define PIN_PHOTOREFLECTOR  22    

#define POT_MIN_1 0
#define POT_MAX_1 320 //[°]

#define POT_MIN_2 0
#define POT_MAX_2 255 //[°]

#define PWM_MAX 1023

float crawler_length  = 250.0; //クローラーの長さ[mm]
float PPR             = 4096.0;
float run_PP          = crawler_length / PPR; //1パルス当たりの走行距離[mm]

float Kp_velocity_l   = 0.027; //50[cm/s]と旋回
//float Kp_velocity_l   = 0.025; //25[cm/s]

float Ki_velocity_l   = 0; //50[cm/s]と旋回
//float Ki_velocity_l   = 0.06; //25[cm/s]

float Kd_velocity_l   = 0.00016; //50[cm/s]と旋回
//float Kd_velocity_l   = 0.00014; //25[cm/s]

float Kp_velocity_r   = 0.026;
float Ki_velocity_r   = 0;
float Kd_velocity_r   = 0.00015;

float Kp_displacement_l = 0.119;
float Ki_displacement_l = 0;
float Kd_displacement_l = 0;
float Kp_displacement_r = 0.12;
float Ki_displacement_r = 0;
float Kd_displacement_r = 0;

float ratio_dis_RperL = 2 / 2;  //直線時の右クローラと左クローラの移動距離比
float one_round_meter = 1.4;   //一回転時の片クローラの移動距離[m]

int   control_period  = 10;     //制御周期
int   pwm_limitter_H  = 320;     //pwmの最大値
int   pwm_limitter_L  = -320;    //pwmの最小値
int   motor_l_offset  = 0;
int   motor_r_offset  = 0;
int   dead_zone       = 200;     //pwmの最小値(絶対値)

float Kp_joint1 = 7.2;
float Ki_joint1 = 0;
float Kd_joint1 = 0.2;
float Kp_pot    = 0.2;
float Kp_joint1_dead_zone = 1.45;

int   joint1_pwm_limitter_H  = 350;     //pwmの最大値
int   joint1_pwm_limitter_L  = -350;    //pwmの最小値
int   joint1_dead_zone       = 170;     //pwmの最小値(絶対値)  
int   joint1_ang_center      = 150;
int   joint1_ang_limitter_H  = joint1_ang_center + 60;   //角度の最大値[度]
int   joint1_ang_limitter_L  = joint1_ang_center - 60;     //角度の最小値[度]


float Kp_joint2 = 7;
float Ki_joint2 = 0;
float Kd_joint2 = 0.1;
float Kp_joint2_dead_zone = 1.2;

int   joint2_pwm_limitter_H  = 320;     //pwmの最大値
int   joint2_pwm_limitter_L  = -320;    //pwmの最小値
int   joint2_dead_zone       = 130;     //pwmの最小値(絶対値)
int   joint2_ang_center      = 170;
int   joint2_ang_limitter_H  = joint2_ang_center + 90;   //角度の最大値[度]
int   joint2_ang_limitter_L  = joint2_ang_center - 90;     //角度の最小値[度]

const byte joint3ID = 1; //第三関節のシリアルサーボID
const byte joint4ID = 1;//第四関節のシリアルサーボID

const int SCS_MAX_VEL = 60; // 第三,四関節_vel=200の時の速度 [度/s]
int joint3_vel = 1; // (0-60) 度/s 
int joint4_vel = 1; // (0-60) 度/s 


int   joint3_ang_center      = 150;
int   joint3_ang_limitter_H  = joint3_ang_center + 75;   //角度の最大値[度]
int   joint3_ang_limitter_L  = joint3_ang_center - 75;     //角度の最小値[度]

int   joint4_ang_center      = 180;
int   joint4_ang_limitter_H  = joint4_ang_center + 75;   //角度の最大値[度]
int   joint4_ang_limitter_L  = joint4_ang_center - 75;;     //角度の最小値[度]
