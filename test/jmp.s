main:
	lda #$42
	sta $FFFC
	jmp main

test:
	lda #$42
	sta $AAAA
	jmp test


