#!/usr/bin/bash
set -x

OUT=$1
mkdir -p $OUT
echo "결과" > $OUT/result.txt
cat $OUT/result.txt
