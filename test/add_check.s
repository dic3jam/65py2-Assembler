variablea = %11111111
variableb = $42


main:
	nop
	nop
	jsr thatThing
	nop
	jmp main

thatThing:
	nop
	nop
	lda #$42
	ora variablea
	sta $8002
	rts

