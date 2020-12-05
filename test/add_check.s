variable1 = %11111111
variable2 = $42


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
	ora variable1
	sta $8002
	rts

