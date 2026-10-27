#!/usr/bin/bash

if [ -z "$1" ]
then
echo "usage: $0 fasta min"
exit 1
fi
if [ -z "$2" ]
then
echo "usage: $0 fasta min"
exit 1
fi
if [ ! -f "$1" ]
then
echo "no file $1"
exit 1
fi
x=$(echo "$2" | tr -d "0-9")
if [ -n "$x" ]
then
echo "$2 is not number"
exit 1
fi

n=0
for l in $(grep -v ">" "$1")
do
if [ ${#l} -lt $2 ]
then
n=$((n+1))
fi
done
echo $n