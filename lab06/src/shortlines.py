#!/usr/bin/env python3
# shortlines.py — FASTA 파일에서 최소 길이보다 짧은 서열 줄의 개수를 출력한다
# 사용법: python3 shortlines.py <FASTA 파일> <최소 길이>

import sys
import os

# bash: if [ -z "$1" ] ... / if [ -z "$2" ] ...  (두 개를 한 번에 검사)
if len(sys.argv) < 3:
    print("사용법: python3 shortlines.py <FASTA 파일> <최소 길이>")
    sys.exit(1)

filename = sys.argv[1]     # bash: $1
min_len = sys.argv[2]      # bash: $2  (아직 글자 상태)

# bash: if [ ! -f "$1" ] ...
if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(1)

# bash: x=$(echo "$2" | tr -d "0-9"); if [ -n "$x" ] ...
if not min_len.isdigit():
    print("오류: 숫자가 아닙니다:", min_len)
    sys.exit(1)

min_len = int(min_len)     # 글자 "16" → 숫자 16

# bash: n=0; for l in $(grep -v ">" "$1"); do ... done; echo $n
n = 0
with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if not line.startswith(">"):        # bash: grep -v ">"
            if len(line) < min_len:         # bash: [ ${#l} -lt $2 ]
                n = n + 1                   # bash: n=$((n+1))
print(n)