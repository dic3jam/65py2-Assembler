variablea = $AFFA
variableb = $AD21
variablec = %00000011

main:
	lda #$42
	sta variablea
	rol
	lda #$43
	sta variableb
	ora %11111111
	sta $8000

