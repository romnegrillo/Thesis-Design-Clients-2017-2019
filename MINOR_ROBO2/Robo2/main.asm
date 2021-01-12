;PIC Configuration
__config _LVP_OFF & _XT_OSC & _WDT_OFF & _PWRTE_ON & _CP_OFF & _BODEN_OFF & _DEBUG_OFF 
    
    list p=16f877
    include "p16f877.inc"
    
    org 0x000
    goto Start
    org 0x004
    
Interrupt
    
    retfie
    
Start
    
    bsf STATUS, RP0	;Bank 1
    bcf STATUS, RP1
    
    movlw B'00000010'	 ; PORT B1 input.
    movwf TRISB		 
    
    movlw B'00000000'	 ; All PORTC output.
    movwf TRISC
    
    bcf STATUS, RP0	;Bank 0
    bcf STATUS, RP1
    
    clrf PORTB		;Initialize PORTB and PORTC by clearing it.
    clrf PORTC
    
    movlw B'10101010'	;Alternate lights on PORTC
    movwf PORTC
    
ReadButton
 
    btfss PORTB,1	;Read PORTB, bit 2 input.
    goto LEDOff		;Bit test f skip if set. If pressed, we on the LED.
    
LEDOn			;LED On
 
    movlw B'01010101'
    movwf PORTC
    goto ReadButton
    
LEDOff			;LED Off
 
    movlw B'10101010'
    movwf PORTC
    goto ReadButton
    
    end
    
    
    
    
    














