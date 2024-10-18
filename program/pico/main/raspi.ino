void check_raspy(){
  int inc_bytes[64] = {-1,};

    /*ここから受信処理*/
    if(Serial.available() > 0){
        if(Serial.read() == 255){
            int sread = 0;
            int idx = 0;
            while(1){
                while(Serial.available() < 1){}
                sread = (int)Serial.read();
                if(sread == 254){
                    break;
                }else if(sread != -1){
                    inc_bytes[idx] = sread;
                    idx += 1;
                }
            }
        }
    }
    /*ここまで*/


    /*ここから受信データに応じた処理*/
    if(inc_bytes[0] == -1){
        //なんもなければ終了
        return;
    }
    switch(inc_bytes[0]){
        case 1:
            run_debug();
            break;
            
        case 2:
        

            break;
        default:
            break;
    }


}
