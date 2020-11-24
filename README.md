# 65py2 Assembler - A 6502 Assembler written in Python

A simple assembler for 6502 assembly files based loosely around old-style syntax. This assembler has been developed as part of @geohot's From The Transistor series, and also as a school project.

Project Status:
Still in development, As of 24NOV2020 I have "happy path" "stability" and am beginning unit nad integration testing

TODO:
write test plan (another school assignment)
unit testing 
integration testing
Write a quick guide to use
Codify rules for someone who is used to a professionally developed assembler such as vasm


Quick rules for use:
2 blank lines needed at end of file
function headers are left adjusted with a : at the end
commands are 1 tab from left
1 blank line separation between functions
must have at least 1 function - the assembler reads in from function headers
less likely for error if all variable assignments at start
must have a .s or .asm extension

Recommended assembly file structure:

variable1 = $FFFC
variable2 = %01010101

main:
	lda #$42
	sta variable1
	jmp main
*\n
\n
