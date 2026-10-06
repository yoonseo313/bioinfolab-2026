#!/usr/bin/env python3
# mkproject.py - 프로젝트 이름을 인자로 받아 data, doc, src 폴더와 doc/README를 만든다
# 사용법: mkproject.py <프로젝트 이름>

import sys
import os
from datetime import datetime

if len(sys.argv) < 2:
    print("사용법:", sys.argv[0], "<프로젝트 이름>")
    print("    주어진 이름으로 data, doc, src 폴더를 가진 프로젝트 폴더를 만든다")
    sys.exit(1)

name = sys.argv[1]

if os.path.isdir(name):
    print("오류: 같은 이름의 폴더가 이미 있습니다:", name)
    sys.exit(1)

os.makedirs(name + "/data")
os.makedirs(name + "/doc")
os.makedirs(name + "/src")

with open(name + "/doc/README", "w") as f:
    f.write("프로젝트: " + name + "\n")
with open(name + "/doc/README", "a") as f:
    f.write("생성일: " + str(datetime.now()) + "\n")

print(name, "프로젝트를 만들었습니다.")
for folder, subfolders, files in os.walk(name):
    print(folder, subfolders, files)