void recieve(){
  if(digitalRead(MR8_B_PIN) == HIGH){
    A1 = 
  }
}

 
//割り込み処理
void chAChangeInterupt()
{
  unsigned long nowPulse = micros();  //現在のマイコン内の時間をnowPulseに代入
  if(digitalRead(MR8_A_PIN) == HIGH)  //端子がHIGHの場合
  {
    startPulse[0]= nowPulse;          //現在の時間をstartPulseに代入
  }
  else                                //端子がLOWの場合
  {
    getPulse[0] = nowPulse - startPulse[0];  //現在の時間(NowPulse)とstartPulseの差を求める=>パルス幅
  }
}
 