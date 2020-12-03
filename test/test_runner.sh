#!/bin/bash

# run this script from the main directory

echo unit tests
echo
echo

python3 -m unittest discover -v

echo
echo
sleep 3

echo integration tests
echo 

i=0
checks=(check1.s check2.s check3.s)

function int_test() {

echo Integration test "$1":

vasm -Fbin -quiet test/"$1"
hexdump -C a.out >> result-vasm
rm a.out
echo

python3 main.py test/"$1"
hexdump -C a.out >> result-65py2
rm a.out
echo

echo Diff:
diff result-vasm result-65py2
rm result-vasm result-65py2

echo
echo

return

}

for i in "${checks[@]}"; do
	int_test "$i"
done

: << 'END'
#test 1

vasm -Fbin test/check1.s
hexdump -C a.out >> result1-vasm
rm a.out

python3 main.py test/check1.s
hexdump -C a.out >> result1-65py2
rm a.out

echo Integration test 1:
diff result1-vasm result1-65py2

echo
echo

#test 2

vasm -Fbin test/check2.s
hexdump -C a.out >> result2-vasm
rm a.out

python3 main.py test/check2.s
hexdump -C a.out >> result2-65py2
rm a.out

echo Integration test 2:
diff result2-vasm result2-65py2

rm result*

END
