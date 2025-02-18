/**
  Generated Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This is the main file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  Description:
    This header file provides implementations for driver APIs for all modules selected in the GUI.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.81.7
        Device            :  PIC16F1938
        Driver Version    :  2.00
*/

/*
    (c) 2018 Microchip Technology Inc. and its subsidiaries. 
    
    Subject to your compliance with these terms, you may use Microchip software and any 
    derivatives exclusively with Microchip products. It is your responsibility to comply with third party 
    license terms applicable to your use of third party software (including open source software) that 
    may accompany Microchip software.
    
    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER 
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY 
    IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS 
    FOR A PARTICULAR PURPOSE.
    
    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, 
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND 
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP 
    HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO 
    THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL 
    CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT 
    OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS 
    SOFTWARE.
*/

#include "mcc_generated_files/mcc.h"

/*
                         Main application
 */
//割り込み周期  :    1ms
//制御周期      :   10ms

//chopper
uint16_t OVD_voltage_adc;       //現在のadc検出電圧
uint16_t OVD_voltage_adc_sb;    //1ステップ前のadc検出電圧
uint16_t target_voltage;        //目標電圧
uint16_t switch_duty = 0;       //10bit

const double correction_value = 5.000 / 4.000;// : 5.000 / 4.697
double OVD_voltage;              //現在の出力電圧
double OVD_voltage_sb;           //1ステップ前の 
double OVD_voltage_tgt = /*6.0*/12.0 * correction_value;   //目標出力電圧

//chopper PID
float P_chop = 1.0;//1.0;//1.0;//1.0;//1.0;//1.0       //Pゲイン
float I_chop = 0.005;//0.0075;////0.0075;//0.0075;////0.0;//0.000001;       //Iゲイン
float D_chop = 0;//0.0000001;//0.0005;//0.0;//0.0001;//2.83;//1.9;       //Dゲイン

double err_vol;
double err_vol_sb;
double err_vol_propotional;
double err_vol_integral;
double err_vol_differential;

//battery
uint16_t BATTVD_voltage_adc;                //adc検出バッテリー電圧
double BATTVD_voltage;                       //バッテリー電圧
const float CUTOFF_BATT_VOLTAGE = 24.0;     //discharge depth 60% : 26.02V


#define CNV_WAIT   0x00
#define CNV_INIT   0x01
#define CNV_OUTPUT 0x02
#define BATTVD_OVD 0x50
#define BATTVD_LVD 0x51
#define CNV_OVD    0xF0
#define CNV_LVD    0xF1
uint8_t CNV_state = CNV_WAIT;

void ISR_SetCNVPWM(void);

void main(void)
{
    // initialize the device
    SYSTEM_Initialize();
    
    TMR6_SetInterruptHandler(ISR_SetCNVPWM);

    // When using interrupts, you need to set the Global and Peripheral Interrupt Enable bits
    // Use the following macros to:

    // Enable the Global Interrupts
    INTERRUPT_GlobalInterruptEnable();

    // Enable the Peripheral Interrupts
    INTERRUPT_PeripheralInterruptEnable();

    // Disable the Global Interrupts
    //INTERRUPT_GlobalInterruptDisable();

    // Disable the Peripheral Interrupts
    //INTERRUPT_PeripheralInterruptDisable();
    //TMR6_StartTimer();
    __delay_ms(250);//スタート待ち1[s]]
    CNV_state = CNV_INIT;
    while (1)
    {
        //update voltage
        BATTVD_voltage_adc  = ADC_GetConversion(BATTVD);
        BATTVD_voltage      = (BATTVD_voltage_adc * 30.0) / 1024.0;
        
        /*
        if(BATTVD_voltage < CUTOFF_BATT_VOLTAGE){
            CNV_state = BATTVD_LVD;
        }
        */
        
        //test only program
        //uint16_t Duty_Buff = 1024 * (BATTVD_voltage / 24.0);
        PWM4_LoadDutyValue(switch_duty/*512*/);
        
        
    }
}

void ISR_SetCNVPWM(void){
    OVD_voltage_adc     = ADC_GetConversion(OVD);
    OVD_voltage         = ((float)OVD_voltage_adc * 30.0) / 1024.0;
    
    if((CNV_state == CNV_OUTPUT) && (1024.0 <= OVD_voltage)){
        //CNV_state = CNV_OVD;
    }
    
    err_vol_sb = err_vol;
    OVD_voltage_sb = OVD_voltage;
    err_vol = OVD_voltage_tgt - OVD_voltage;
    err_vol_propotional = err_vol;
    err_vol_integral = err_vol + (err_vol * 0.01);
    err_vol_differential = (err_vol - err_vol_sb) / 0.010;
    
    switch(CNV_state){
        case CNV_INIT:
            if(switch_duty < 512/*OVD_voltage < OVD_voltage_tgt*/){  //682
                switch_duty += 2;
            }else{
                CNV_state = CNV_OUTPUT;
            }
            break;
        
        case CNV_OUTPUT:
            //switch_duty = 512;
            switch_duty = (uint16_t)((OVD_voltage + P_chop * err_vol_propotional + I_chop * err_vol_integral + D_chop * err_vol_differential) * 1024.0) / 24.0;
            break;
            
        case CNV_OVD:
            switch_duty = 0;
            break;
    }
}
/**
 End of File
*/