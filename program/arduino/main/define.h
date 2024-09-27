#define PIN_ENC_A_L  2
#define PIN_ENC_B_L  4
#define PIN_ENC_A_R  3
#define PIN_ENC_B_R  7
#define PIN_DIR_R    8
#define PIN_PWM_R    9
#define PIN_DIR_L   12
#define PIN_PWM_L   11
#define PIN_SW      10
#define PIN_LED     13
#define PIN_BATT    19 


float crawler_length  = 250.0; //クローラーの長さ[mm]
float PPR             = 4096.0;
float run_PP          = crawler_length / PPR; //1パルス当たりの走行距離[mm]

float Kp_velocity_l   = 0.027; //50[cm/s]と旋回
//float Kp_velocity_l   = 0.025; //25[cm/s]

float Ki_velocity_l   = 0.065; //50[cm/s]と旋回
//float Ki_velocity_l   = 0.06; //25[cm/s]

float Kd_velocity_l   = 0.00016; //50[cm/s]と旋回
//float Kd_velocity_l   = 0.00014; //25[cm/s]

float Kp_velocity_r   = 0.026;
float Ki_velocity_r   = 0.062;
float Kd_velocity_r   = 0.00015;

float Kp_displacement_l = 0.119;
float Ki_displacement_l = 0.0027;
float Kd_displacement_l = 0;
float Kp_displacement_r = 0.12;
float Ki_displacement_r = 0.0027;
float Kd_displacement_r = 0;

int   control_period  = 10;
int   pwm_limitter_H  = 80;
int   pwm_limitter_L  = -80;
int   motor_l_offset  = 0;
int   motor_r_offset  = 0;
int   dead_zone       = 40;

int   T_GIVE          = 100;  //[sec]
