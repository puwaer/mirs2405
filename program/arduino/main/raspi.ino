/*void check_serial(){
    int inc_bytes[64] = {-1,};

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

    if(inc_bytes[0] == -1){
      return;
    }
    switch(inc_bytes[0]){
        case 1:
            // ***();
            break;
        
        case 2:
            
            break;
        
        case 3:
            
            break;
        
        case 4:
            
            break;
        
        case 5:
            
            break;
        
        case 6:
            
            break;
        
        case 7:
            
            break;
        
        case 8:
            
            break;
        
        case 9:
            
            break;
        
        case 10:
            
            break;

        case 11:
            
            break;

        default:
            break;
    }


}*/




int buffer_size = 9;

byte received_data[9];

void raspi_receive_person(float *a){
  while(1){
    if(Serial.available() >= buffer_size){
      Serial.readBytes(received_data, buffer_size);
      
      byte header = received_data[0];

      if(header == 001){
        int received_command[1];
      
        for(int i = 0; i < 1; i++){
          received_command[i] = received_data[1 + i *2] | (received_data[2 + i *2] << 8);
        }
        *a = received_command[0];
        break;
      }
    }
    else{
      Serial.println("The data must be 9 bytes");
      Serial.println("Please send the data again");
      delay(1000);
    }
  }
}

void raspi_receive_coordinate(float *a, float *b, float *c, float *d, float *e, float *f, float *g){
  while(1){
    if(Serial.available() >= buffer_size){
      Serial.readBytes(received_data, buffer_size);
      
      byte header = received_data[0];

      if(header == 010){
        int received_command[7];
      
        for(int i = 0; i < 7; i++){
          received_command[i] = received_data[1 + i *2] | (received_data[2 + i *2] << 8);
        }
        *a = received_command[0];
        *b = received_command[1];
        *c = received_command[2];
        *d = received_command[3];
        *e = received_command[4];
        *f = received_command[5];
        *g = received_command[6];
        break;
      }
    }
    else{
      Serial.println("The data must be 9 bytes");
      Serial.println("Please send the data again");
      delay(1000);
    }
  }
}