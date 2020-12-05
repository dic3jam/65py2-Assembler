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
cat test/"$1"
vasm -Fbin -quiet test/"$1"
hexdump -C a.out >> result-vasm
rm a.out

python3 main.py test/"$1"
hexdump -C a.out >> result-65py2
rm a.out

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

