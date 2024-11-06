#define PIN_GRIPPER_PWM     3   //グリッパー開閉
#define PIN_AIRCHUCK_1_PWM  5   //エアーチャックの昇降
#define PIN_AIRCHUCK_2_PWM  6   //エアーチャックの昇降

#define PIN_TURNTABLEENC_A  2     //ターンテーブル
#define PIN_TURNTABLEENC_B  4
#define PIN_TURNTABLE_PWM   10  
#define PIN_TURNTABLE_DIR   7

#define PIN_PUMP_PWM        9   //真空ポンプ
#define PIN_PUMP_DIR        12


#define GRIP_MIN 544  //サーボの角度が0度のときのパルス幅[us]。デフォルトは544。
#define GRIP_MAX 2400 // サーボの角度が180度のときのパルス幅[us]。デフォルトは2400。
#define GRIP_OPEN_ANG 15  //グリッパーの動作角度[度](0-180)
#define GRIP_CLOSE_ANG 0

#define AIRCHUCK_MIN  544
#define AIRCHUCK_MAX  2400
#define AIRCHUCK_ANG  15

#define PPR  4096.0

float Kp_turntable = 0.119;
float Ki_turntable = 0;
float Kd_turntable = 0;

int   turntable_pwm_limitter_H  = 80;     //pwmの最大値
int   turntable_pwm_limitter_L  = -80;    //pwmの最小値
int   turntable_dead_zone       = 50;     //pwmの最小値(絶対値)

int   pump_pwm  = 60;
int   pump_time = 1000; //[ms]

int   control_period  = 10;     //制御周期[ms]
