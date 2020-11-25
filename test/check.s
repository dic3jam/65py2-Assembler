variablea = $AFFA
variableb = $AD21
variablec = %00000011

main:
	lda #$42
	sta variablea
	rol
	bcc
	jsr test
	jmp main

test:
	rts


