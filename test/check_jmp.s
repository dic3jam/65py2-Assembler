main:
	lda #$42
	sta $8000
	jsr doThatThing
	jsr otherThing
	jmp main

doThatThing:
	lda #$42
	sta $8002
	rts

otherThing:
	rol
	rts

