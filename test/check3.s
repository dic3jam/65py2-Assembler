PORTB = $6000
PORTA = $6001
DDRB = $6002
DDRA = $6003
message = $6004
value = $6005
number = $6006

E = %10000000
RW = %01000000
RS = %00100000
CLR = %00000001
RH = %00000010


main:
	lda #%11111111 
	sta DDRB
	lda #%11100000
	sta DDRA
	lda #%00111000 
	jsr lcd_instruction	
	lda #%00001110
	jsr lcd_instruction
	lda #%00000110 
	jsr lcd_instruction
	lda #CLR 
	jsr lcd_instruction
	lda #0
	sta message
	lda number
	sta value
	lda number
	sta value
	jmp main

lcd_wait:
	pha 
	lda #%00000000 
	sta DDRB
	lda #RW
	sta PORTA
	lda #RW 
	sta PORTA	
	lda PORTB
	and #%10000000
	sta PORTA
	lda #%11111111 
	sta DDRB	
	rts	

lcd_instruction:
	jsr lcd_wait
	sta PORTB
	lda #0
	sta PORTA
	lda #E
	sta PORTA
	lda #0
	sta PORTA
	rts

	