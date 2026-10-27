#!/usr/bin/bash
# mkproject2.sh — 프로젝트 이름을 인자로 받아 data, doc, src 폴더와 doc/README 파일을 만든다
# 사용법: mkproject2.sh <프로젝트 이름>

if [ -z "$1" ]
then
    echo "사용법: $0 <프로젝트 이름>"
    echo "   주어진 이름으로 data, doc, src 폴더를 가진 프로젝트 폴더를 만듭니다."
    exit 1
fi

NAME="$1"

if [ -d "$NAME" ]
then
    echo "오류: 같은 이름의 폴더가 이미 있습니다: $NAME"
    exit 1
fi

mkdir -p "$NAME/data" "$NAME/doc" "$NAME/src"
echo "프로젝트: $NAME" > "$NAME/doc/README"
echo "생성일: $(date)" >> "$NAME/doc/README"

echo "$NAME 프로젝트를 만들었습니다."
ls -R "$NAME"