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

// get/set BATTVD aliases
#define BATTVD_TRIS                 TRISAbits.TRISA0
#define BATTVD_LAT                  LATAbits.LATA0
#define BATTVD_PORT                 PORTAbits.RA0
#define BATTVD_ANS                  ANSELAbits.ANSA0
#define BATTVD_SetHigh()            do { LATAbits.LATA0 = 1; } while(0)
#define BATTVD_SetLow()             do { LATAbits.LATA0 = 0; } while(0)
#define BATTVD_Toggle()             do { LATAbits.LATA0 = ~LATAbits.LATA0; } while(0)
#define BATTVD_GetValue()           PORTAbits.RA0
#define BATTVD_SetDigitalInput()    do { TRISAbits.TRISA0 = 1; } while(0)
#define BATTVD_SetDigitalOutput()   do { TRISAbits.TRISA0 = 0; } while(0)
#define BATTVD_SetAnalogMode()      do { ANSELAbits.ANSA0 = 1; } while(0)
#define BATTVD_SetDigitalMode()     do { ANSELAbits.ANSA0 = 0; } while(0)

// get/set OVD aliases
#define OVD_TRIS                 TRISAbits.TRISA1
#define OVD_LAT                  LATAbits.LATA1
#define OVD_PORT                 PORTAbits.RA1
#define OVD_ANS                  ANSELAbits.ANSA1
#define OVD_SetHigh()            do { LATAbits.LATA1 = 1; } while(0)
#define OVD_SetLow()             do { LATAbits.LATA1 = 0; } while(0)
#define OVD_Toggle()             do { LATAbits.LATA1 = ~LATAbits.LATA1; } while(0)
#define OVD_GetValue()           PORTAbits.RA1
#define OVD_SetDigitalInput()    do { TRISAbits.TRISA1 = 1; } while(0)
#define OVD_SetDigitalOutput()   do { TRISAbits.TRISA1 = 0; } while(0)
#define OVD_SetAnalogMode()      do { ANSELAbits.ANSA1 = 1; } while(0)
#define OVD_SetDigitalMode()     do { ANSELAbits.ANSA1 = 0; } while(0)

// get/set RB0 procedures
#define RB0_SetHigh()            do { LATBbits.LATB0 = 1; } while(0)
#define RB0_SetLow()             do { LATBbits.LATB0 = 0; } while(0)
#define RB0_Toggle()             do { LATBbits.LATB0 = ~LATBbits.LATB0; } while(0)
#define RB0_GetValue()              PORTBbits.RB0
#define RB0_SetDigitalInput()    do { TRISBbits.TRISB0 = 1; } while(0)
#define RB0_SetDigitalOutput()   do { TRISBbits.TRISB0 = 0; } while(0)
#define RB0_SetPullup()             do { WPUBbits.WPUB0 = 1; } while(0)
#define RB0_ResetPullup()           do { WPUBbits.WPUB0 = 0; } while(0)
#define RB0_SetAnalogMode()         do { ANSELBbits.ANSB0 = 1; } while(0)
#define RB0_SetDigitalMode()        do { ANSELBbits.ANSB0 = 0; } while(0)

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