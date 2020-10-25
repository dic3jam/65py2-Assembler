object1 = %11111111
object2 = $FFFF
object3 = 255

 .org $8000

function1:

	lda #object1
	sta $2000
	lda #$FF
	rol 
	sec
	adc 10
	sta $2002

function2:
	jmp function1

