ADDRESS = %11111111
CHECK = $FF

function1:
	lda $10
	sta ADDRESS

function2:
	ora $10
	eor 25
function1

function3:
	lda CHECK
	sta ADDRESS

function4:
	lda ADDRESS
	sta CHECK

