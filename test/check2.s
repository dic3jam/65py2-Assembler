variablea = $42


main:
	lda #$42
	sta $8000
	lda #$43
	ora %11111111
	sta $8002
	jmp main


