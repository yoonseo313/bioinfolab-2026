#!/usr/bin/bash
# batchinfo.sh — 폴더 안의 모든 FASTA 파일에 대해 파일 이름과 서열 개수를 탭으로 구분해 출력한다
# 사용법: batchinfo.sh <폴더 이름>

if [ -z "$1" ]
then
    echo "사용법: $0 <폴더 이름>"
    echo "   폴더 안 FASTA 파일들의 서열 개수를 표로 출력합니다."
    exit 1
fi

DIR="$1"

# 3단계: 폴더가 존재하는지 검사
if [ ! -d "$DIR" ]
then
    echo "오류: 폴더를 찾을 수 없습니다: $DIR"
    exit 1
fi

cd "$DIR"

# 4단계: FASTA 파일이 하나도 없으면 *.fasta 가 글자 그대로 넘어오므로 검사
for F in *.fasta
do
    if [ ! -f "$F" ]
    then
        echo "오류: $DIR 폴더에 FASTA 파일이 없습니다."
        exit 1
    fi
done

echo "file count" | tr " " "\t"
for F in *.fasta
do
    N=$(grep -c ">" "$F")
    echo "$F $N" | tr " " "\t"
done