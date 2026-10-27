#!/usr/bin/bash
# fastainfo.sh - FASTA 파일의 기본 정보를 출력한다
# 사용법: fastainfo.sh <FASTA 파일>

if [ -z "$1" ]
then
    echo "사용법: $0 <FASTA 파일>"
    echo "   주어진 FASTA 파일의 요약 정보를 출력합니다."
    exit 1
fi

if [ ! -f "$1" ]
then
    echo "오류: 파일을 찾을 수 없습니다: $1"
    exit 1
fi

FILE="$1"

N=$(grep -c ">" "$FILE")
SEQ=$(grep -v ">" "$FILE" | tr -d "\n")
LEN=${#SEQ}

echo "파일: $FILE"
echo "서열 개수: $N"
echo "서열 이름:"
grep ">" "$FILE" | cut -d " " -f1 | tr -d ">" | sed 's/^/  /'
echo "총 염기 수(대략): $LEN"
