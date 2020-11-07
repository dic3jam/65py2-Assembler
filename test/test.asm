object1 = %11111111
object2 = $FFFD
object3 = 255
THAT = $AD02
willNotWork = $KL21

 .org $8000

function1:
	lda #object1
	sta $2000
test6=$1234
	lda #$FF
	rol 
	sec
	adc 10
	sta $2002

test5=123
blah = 002

function2:
	jmp function1



