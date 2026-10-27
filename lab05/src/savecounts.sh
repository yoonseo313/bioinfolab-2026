#!/usr/bin/bash
# savecounts.sh — 폴더 안 FASTA 파일별 서열 개수를 "이름<탭>개수" 형식으로 파일에 저장한다
# 사용법: savecounts.sh <폴더> <저장할 파일>

DIR="$1"
OUT="$2"

for F in "$DIR"/*.fasta
do
    NAME=$(echo "$F" | cut -d "/" -f2)
    N=$(grep -c ">" "$F")
    echo "$NAME $N" | tr " " "\t" >> "$OUT"
done