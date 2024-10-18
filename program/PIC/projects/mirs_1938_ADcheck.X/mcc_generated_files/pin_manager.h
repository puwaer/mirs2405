/**
  @Generated Pin Manager Header File

  @Company:
    Microchip Technology Inc.

  @File Name:
    pin_manager.h

  @Summary:
    This is the Pin Manager file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  @Description
    This header file provides APIs for driver for .
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.81.7
        Device            :  PIC16F1938
        Driver Version    :  2.11
    The generated drivers are tested against the following:
        Compiler          :  XC8 2.31 and above
        MPLAB 	          :  MPLAB X 5.45	
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

#ifndef PIN_MANAGER_H
#define PIN_MANAGER_H

/**
  Section: Included Files
*/

#include <xc.h>

#define INPUT   1
#define OUTPUT  0

#define HIGH    1
#define LOW     0

#define ANALOG      1
#define DIGITAL     0

#define PULL_UP_ENABLED      1
#define PULL_UP_DISABLED     0

// get/set channel_AN0 aliases
#define channel_AN0_TRIS                 TRISAbits.TRISA0
#define channel_AN0_LAT                  LATAbits.LATA0
#define channel_AN0_PORT                 PORTAbits.RA0
#define channel_AN0_ANS                  ANSELAbits.ANSA0
#define channel_AN0_SetHigh()            do { LATAbits.LATA0 = 1; } while(0)
#define channel_AN0_SetLow()             do { LATAbits.LATA0 = 0; } while(0)
#define channel_AN0_Toggle()             do { LATAbits.LATA0 = ~LATAbits.LATA0; } while(0)
#define channel_AN0_GetValue()           PORTAbits.RA0
#define channel_AN0_SetDigitalInput()    do { TRISAbits.TRISA0 = 1; } while(0)
#define channel_AN0_SetDigitalOutput()   do { TRISAbits.TRISA0 = 0; } while(0)
#define channel_AN0_SetAnalogMode()      do { ANSELAbits.ANSA0 = 1; } while(0)
#define channel_AN0_SetDigitalMode()     do { ANSELAbits.ANSA0 = 0; } while(0)

// get/set dig4 aliases
#define dig4_TRIS                 TRISBbits.TRISB0
#define dig4_LAT                  LATBbits.LATB0
#define dig4_PORT                 PORTBbits.RB0
#define dig4_WPU                  WPUBbits.WPUB0
#define dig4_ANS                  ANSELBbits.ANSB0
#define dig4_SetHigh()            do { LATBbits.LATB0 = 1; } while(0)
#define dig4_SetLow()             do { LATBbits.LATB0 = 0; } while(0)
#define dig4_Toggle()             do { LATBbits.LATB0 = ~LATBbits.LATB0; } while(0)
#define dig4_GetValue()           PORTBbits.RB0
#define dig4_SetDigitalInput()    do { TRISBbits.TRISB0 = 1; } while(0)
#define dig4_SetDigitalOutput()   do { TRISBbits.TRISB0 = 0; } while(0)
#define dig4_SetPullup()          do { WPUBbits.WPUB0 = 1; } while(0)
#define dig4_ResetPullup()        do { WPUBbits.WPUB0 = 0; } while(0)
#define dig4_SetAnalogMode()      do { ANSELBbits.ANSB0 = 1; } while(0)
#define dig4_SetDigitalMode()     do { ANSELBbits.ANSB0 = 0; } while(0)

// get/set dig3 aliases
#define dig3_TRIS                 TRISBbits.TRISB1
#define dig3_LAT                  LATBbits.LATB1
#define dig3_PORT                 PORTBbits.RB1
#define dig3_WPU                  WPUBbits.WPUB1
#define dig3_ANS                  ANSELBbits.ANSB1
#define dig3_SetHigh()            do { LATBbits.LATB1 = 1; } while(0)
#define dig3_SetLow()             do { LATBbits.LATB1 = 0; } while(0)
#define dig3_Toggle()             do { LATBbits.LATB1 = ~LATBbits.LATB1; } while(0)
#define dig3_GetValue()           PORTBbits.RB1
#define dig3_SetDigitalInput()    do { TRISBbits.TRISB1 = 1; } while(0)
#define dig3_SetDigitalOutput()   do { TRISBbits.TRISB1 = 0; } while(0)
#define dig3_SetPullup()          do { WPUBbits.WPUB1 = 1; } while(0)
#define dig3_ResetPullup()        do { WPUBbits.WPUB1 = 0; } while(0)
#define dig3_SetAnalogMode()      do { ANSELBbits.ANSB1 = 1; } while(0)
#define dig3_SetDigitalMode()     do { ANSELBbits.ANSB1 = 0; } while(0)

// get/set dig2 aliases
#define dig2_TRIS                 TRISBbits.TRISB2
#define dig2_LAT                  LATBbits.LATB2
#define dig2_PORT                 PORTBbits.RB2
#define dig2_WPU                  WPUBbits.WPUB2
#define dig2_ANS                  ANSELBbits.ANSB2
#define dig2_SetHigh()            do { LATBbits.LATB2 = 1; } while(0)
#define dig2_SetLow()             do { LATBbits.LATB2 = 0; } while(0)
#define dig2_Toggle()             do { LATBbits.LATB2 = ~LATBbits.LATB2; } while(0)
#define dig2_GetValue()           PORTBbits.RB2
#define dig2_SetDigitalInput()    do { TRISBbits.TRISB2 = 1; } while(0)
#define dig2_SetDigitalOutput()   do { TRISBbits.TRISB2 = 0; } while(0)
#define dig2_SetPullup()          do { WPUBbits.WPUB2 = 1; } while(0)
#define dig2_ResetPullup()        do { WPUBbits.WPUB2 = 0; } while(0)
#define dig2_SetAnalogMode()      do { ANSELBbits.ANSB2 = 1; } while(0)
#define dig2_SetDigitalMode()     do { ANSELBbits.ANSB2 = 0; } while(0)

// get/set dig1 aliases
#define dig1_TRIS                 TRISBbits.TRISB3
#define dig1_LAT                  LATBbits.LATB3
#define dig1_PORT                 PORTBbits.RB3
#define dig1_WPU                  WPUBbits.WPUB3
#define dig1_ANS                  ANSELBbits.ANSB3
#define dig1_SetHigh()            do { LATBbits.LATB3 = 1; } while(0)
#define dig1_SetLow()             do { LATBbits.LATB3 = 0; } while(0)
#define dig1_Toggle()             do { LATBbits.LATB3 = ~LATBbits.LATB3; } while(0)
#define dig1_GetValue()           PORTBbits.RB3
#define dig1_SetDigitalInput()    do { TRISBbits.TRISB3 = 1; } while(0)
#define dig1_SetDigitalOutput()   do { TRISBbits.TRISB3 = 0; } while(0)
#define dig1_SetPullup()          do { WPUBbits.WPUB3 = 1; } while(0)
#define dig1_ResetPullup()        do { WPUBbits.WPUB3 = 0; } while(0)
#define dig1_SetAnalogMode()      do { ANSELBbits.ANSB3 = 1; } while(0)
#define dig1_SetDigitalMode()     do { ANSELBbits.ANSB3 = 0; } while(0)

// get/set seg_A aliases
#define seg_A_TRIS                 TRISCbits.TRISC0
#define seg_A_LAT                  LATCbits.LATC0
#define seg_A_PORT                 PORTCbits.RC0
#define seg_A_SetHigh()            do { LATCbits.LATC0 = 1; } while(0)
#define seg_A_SetLow()             do { LATCbits.LATC0 = 0; } while(0)
#define seg_A_Toggle()             do { LATCbits.LATC0 = ~LATCbits.LATC0; } while(0)
#define seg_A_GetValue()           PORTCbits.RC0
#define seg_A_SetDigitalInput()    do { TRISCbits.TRISC0 = 1; } while(0)
#define seg_A_SetDigitalOutput()   do { TRISCbits.TRISC0 = 0; } while(0)

// get/set seg_B aliases
#define seg_B_TRIS                 TRISCbits.TRISC1
#define seg_B_LAT                  LATCbits.LATC1
#define seg_B_PORT                 PORTCbits.RC1
#define seg_B_SetHigh()            do { LATCbits.LATC1 = 1; } while(0)
#define seg_B_SetLow()             do { LATCbits.LATC1 = 0; } while(0)
#define seg_B_Toggle()             do { LATCbits.LATC1 = ~LATCbits.LATC1; } while(0)
#define seg_B_GetValue()           PORTCbits.RC1
#define seg_B_SetDigitalInput()    do { TRISCbits.TRISC1 = 1; } while(0)
#define seg_B_SetDigitalOutput()   do { TRISCbits.TRISC1 = 0; } while(0)

// get/set seg_C aliases
#define seg_C_TRIS                 TRISCbits.TRISC2
#define seg_C_LAT                  LATCbits.LATC2
#define seg_C_PORT                 PORTCbits.RC2
#define seg_C_SetHigh()            do { LATCbits.LATC2 = 1; } while(0)
#define seg_C_SetLow()             do { LATCbits.LATC2 = 0; } while(0)
#define seg_C_Toggle()             do { LATCbits.LATC2 = ~LATCbits.LATC2; } while(0)
#define seg_C_GetValue()           PORTCbits.RC2
#define seg_C_SetDigitalInput()    do { TRISCbits.TRISC2 = 1; } while(0)
#define seg_C_SetDigitalOutput()   do { TRISCbits.TRISC2 = 0; } while(0)

// get/set seg_D aliases
#define seg_D_TRIS                 TRISCbits.TRISC3
#define seg_D_LAT                  LATCbits.LATC3
#define seg_D_PORT                 PORTCbits.RC3
#define seg_D_SetHigh()            do { LATCbits.LATC3 = 1; } while(0)
#define seg_D_SetLow()             do { LATCbits.LATC3 = 0; } while(0)
#define seg_D_Toggle()             do { LATCbits.LATC3 = ~LATCbits.LATC3; } while(0)
#define seg_D_GetValue()           PORTCbits.RC3
#define seg_D_SetDigitalInput()    do { TRISCbits.TRISC3 = 1; } while(0)
#define seg_D_SetDigitalOutput()   do { TRISCbits.TRISC3 = 0; } while(0)

// get/set seg_E aliases
#define seg_E_TRIS                 TRISCbits.TRISC4
#define seg_E_LAT                  LATCbits.LATC4
#define seg_E_PORT                 PORTCbits.RC4
#define seg_E_SetHigh()            do { LATCbits.LATC4 = 1; } while(0)
#define seg_E_SetLow()             do { LATCbits.LATC4 = 0; } while(0)
#define seg_E_Toggle()             do { LATCbits.LATC4 = ~LATCbits.LATC4; } while(0)
#define seg_E_GetValue()           PORTCbits.RC4
#define seg_E_SetDigitalInput()    do { TRISCbits.TRISC4 = 1; } while(0)
#define seg_E_SetDigitalOutput()   do { TRISCbits.TRISC4 = 0; } while(0)

// get/set seg_F aliases
#define seg_F_TRIS                 TRISCbits.TRISC5
#define seg_F_LAT                  LATCbits.LATC5
#define seg_F_PORT                 PORTCbits.RC5
#define seg_F_SetHigh()            do { LATCbits.LATC5 = 1; } while(0)
#define seg_F_SetLow()             do { LATCbits.LATC5 = 0; } while(0)
#define seg_F_Toggle()             do { LATCbits.LATC5 = ~LATCbits.LATC5; } while(0)
#define seg_F_GetValue()           PORTCbits.RC5
#define seg_F_SetDigitalInput()    do { TRISCbits.TRISC5 = 1; } while(0)
#define seg_F_SetDigitalOutput()   do { TRISCbits.TRISC5 = 0; } while(0)

// get/set seg_G aliases
#define seg_G_TRIS                 TRISCbits.TRISC6
#define seg_G_LAT                  LATCbits.LATC6
#define seg_G_PORT                 PORTCbits.RC6
#define seg_G_SetHigh()            do { LATCbits.LATC6 = 1; } while(0)
#define seg_G_SetLow()             do { LATCbits.LATC6 = 0; } while(0)
#define seg_G_Toggle()             do { LATCbits.LATC6 = ~LATCbits.LATC6; } while(0)
#define seg_G_GetValue()           PORTCbits.RC6
#define seg_G_SetDigitalInput()    do { TRISCbits.TRISC6 = 1; } while(0)
#define seg_G_SetDigitalOutput()   do { TRISCbits.TRISC6 = 0; } while(0)

// get/set seg_DP aliases
#define seg_DP_TRIS                 TRISCbits.TRISC7
#define seg_DP_LAT                  LATCbits.LATC7
#define seg_DP_PORT                 PORTCbits.RC7
#define seg_DP_SetHigh()            do { LATCbits.LATC7 = 1; } while(0)
#define seg_DP_SetLow()             do { LATCbits.LATC7 = 0; } while(0)
#define seg_DP_Toggle()             do { LATCbits.LATC7 = ~LATCbits.LATC7; } while(0)
#define seg_DP_GetValue()           PORTCbits.RC7
#define seg_DP_SetDigitalInput()    do { TRISCbits.TRISC7 = 1; } while(0)
#define seg_DP_SetDigitalOutput()   do { TRISCbits.TRISC7 = 0; } while(0)

/**
   @Param
    none
   @Returns
    none
   @Description
    GPIO and peripheral I/O initialization
   @Example
    PIN_MANAGER_Initialize();
 */
void PIN_MANAGER_Initialize (void);

/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handling routine
 * @Example
    PIN_MANAGER_IOC();
 */
void PIN_MANAGER_IOC(void);



#endif // PIN_MANAGER_H
/**
 End of File
*/