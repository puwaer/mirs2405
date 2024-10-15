#define PIN_ENC_A_L   1
#define PIN_ENC_A_R   2
#define PIN_ENC_B_L   4  
#define PIN_ENC_B_R   5
#define PIN_DIR_R     6
#define PIN_DIR_L     7
#define PIN_PWM_R     9 
#define PIN_PWM_L     10

#define PIN_SCS215_1_PWM    11
#define PIN_SCS215_1_PWM    12

#define PIN_LC578VA_PWM     19
#define PIN_LC578VA_DIR     24

#define PIN_JC578VA_1_PWM   20
#define PIN_JC578VA_1_DIR   25

#define PIN_INFRARED_LED    29
#define PIN_PHOTOREFLECTOR  34

#define PIN_POTENTIOMETER_1 31
#define PIN_POTENTIOMETER_2 32

#define PIN_LED     13
#define PIN_BATT    19    


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
float one_round_meter = 1.35;   //一回転時の片クローラの移動距離[m]

int   control_period  = 10;     //制御周期
int   pwm_limitter_H  = 80;     //pwmの最大値
int   pwm_limitter_L  = -80;    //pwmの最小値
int   motor_l_offset  = 0;
int   motor_r_offset  = 0;
int   dead_zone       = 50;     //pwmの最小値(絶対値)



