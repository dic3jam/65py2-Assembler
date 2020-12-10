# 65py2 Assembler - A 6502 Assembler written in Python

A simple assembler for 6502 assembly files based loosely around old-style syntax. This assembler has been developed as part of @geohot's From The Transistor series, and also as a school project.

### Project Status:
I have completed the third iteration of the assembler which adds jmp and jsr functionality.

### TODO:
Begin fourth iteration:
- full addressing 
- zero page instructions
- comments 
- figure out a binary release	

rewrite test plan to feature new unit tests, create a test results chart and
publish with future iterations

### Quick rules for use:
2 blank lines needed at end of file
function headers are left adjusted with a : at the end
commands are 1 tab from left
1 blank line separation between functions
must have at least 1 function - the assembler reads in from function headers
less likely for error if all variable assignments at start
must have a .s or .asm extension for file to assemble
variable names cannot contain numbers

how to run:

python3 'wherever'/main.py 'wherever'/filetoassemble.s

Recommended assembly file structure:

variable1 = $FFFC
variable2 = %01010101

main:
	lda #$42
	sta variable1
	jmp main
\n
\n
