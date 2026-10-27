#!/usr/bin/env python3
# mkproject.py — 프로젝트 이름을 인자로 받아 data, doc, src 폴더를 만든다
# 사용법: python3 mkproject.py <프로젝트 이름>

import sys
import os

# bash: if [ -z "$1" ]; then ... exit 1; fi
if len(sys.argv) < 2:
    print("사용법: python3 mkproject.py <프로젝트 이름>")
    print("    주어진 이름으로 data, doc, src 폴더를 가진 프로젝트 폴더를 만듭니다.")
    sys.exit(1)

# bash: NAME="$1"
name = sys.argv[1]

# bash: if [ -d "$NAME" ]; then ... exit 1; fi
if os.path.isdir(name):
    print("오류: 같은 이름의 폴더가 이미 있습니다:", name)
    sys.exit(1)

# bash: mkdir -p "$NAME/data" "$NAME/doc" "$NAME/src"
for sub in ["data", "doc", "src"]:
    os.makedirs(name + "/" + sub)

# bash: echo "$NAME 프로젝트를 만들었습니다."
print(name, "프로젝트를 만들었습니다.")