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

void Segments_Init(void);
void Segments_Set(int, int);

uint16_t num            = 0;
uint16_t num_counter    = 0;
uint16_t digit_counter  = 0;
uint16_t count_scale    = 0;

uint16_t AD_CNT = 250;

int32_t Voltage;

const char seg[10] = {
                    0b00111111,//0
                    0b00000110,//1
                    0b01011011,//2
                    0b01001111,//3
                    0b01100110,//4
                    0b01101101,//5
                    0b01111101,//6
                    0b00100111,//7
                    0b01111111,//8
                    0b01101111 //9
                    };

const char digit[4] = {
                    0b00001110,
                    0b00001101,
                    0b00001011,
                    0b00000111
                    };

uint16_t ADC_result;

/*
                         Main application
 */
void main(void)
{
    // initialize the device
    SYSTEM_Initialize();
    
    Segments_Init();
    // When using interrupts, you need to set the Global and Peripheral Interrupt Enable bits
    // Use the following macros to:

    // Enable the Global Interrupts
    //INTERRUPT_GlobalInterruptEnable();

    // Enable the Peripheral Interrupts
    //INTERRUPT_PeripheralInterruptEnable();

    // Disable the Global Interrupts
    //INTERRUPT_GlobalInterruptDisable();

    // Disable the Peripheral Interrupts
    //INTERRUPT_PeripheralInterruptDisable();

    while (1)
    {
        // Add your application code
        if(AD_CNT == 250){
            ADC_result = ADC_GetConversion(channel_AN0);
        }
        float fv = ((ADC_result * 30.0) / 1024.0);
        Voltage = (int32_t)(fv * 100);
        
        Segments_Set(Voltage % 10           ,0);
        __delay_us(500);
        Segments_Set((Voltage / 10) % 10    ,1);
        __delay_us(500);
        Segments_Set((Voltage / 100) % 10   ,2);
        __delay_us(500);
        Segments_Set(Voltage / 1000         ,3);
        __delay_us(500);
        
        AD_CNT--;
        
        if(AD_CNT <= 0){
            AD_CNT = 250;
        }
        
    }
}

void Segments_Init(void){
    for(int z = 3; z >= 0; z--){
        PORTB = digit[z];
        PORTC = 0b00000001;
        for(int i = 1; i <= 7; i++){
            __delay_ms(10);
            PORTC = PORTC << 1;
        }
    }
}

void Segments_Set(int fnc_number, int fnc_digit){
    PORTC = 0b00000000;
    PORTB = digit[fnc_digit];
    PORTC = seg[fnc_number];
    if(fnc_digit == 2){
        seg_DP_SetHigh();
    }else{
        seg_DP_SetLow();
    }
}
/**
 End of File
*/