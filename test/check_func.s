variablea = $42
variableb = 42


main:
	lda variablea
	sta $8000
	jmp main


