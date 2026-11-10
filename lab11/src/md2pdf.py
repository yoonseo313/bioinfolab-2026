# 마크다운(.md) 파일을 한글이 깨지지 않는 PDF 로 바꾸는 스크립트
#
# 사용법 (lab11 폴더 안에서, conda bio 환경의 파이썬으로 실행):
#   /opt/conda/envs/bio/bin/python src/md2pdf.py <입력.md> <출력.pdf> [폰트폴더] [PDF 제목]
#
#   예) /opt/conda/envs/bio/bin/python src/md2pdf.py doc/qual_by_position.md doc/qual_by_position.pdf
#
# - PySide6(Qt) 가 bio 환경에만 있으므로 시스템 python3 로는 실행되지 않는다.
# - 폰트폴더를 생략하면 data/font (나눔고딕, 나눔고딕코딩)를 사용한다.
# - PDF 제목을 생략하면 마크다운의 첫 번째 '# 제목' 줄을 사용한다.
# - 변환 순서: 마크다운 -> HTML (Qt 내장 변환기) -> 글꼴·스타일 보정 -> A4 PDF

import os
import re
import sys

# 화면(디스플레이)이 없는 Codespaces 에서도 Qt 가 돌도록 설정한다
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QTextDocument, QPdfWriter, QPageSize, QPageLayout, QFont
from PySide6.QtCore import QMarginsF

if len(sys.argv) < 3:
    print("사용법: /opt/conda/envs/bio/bin/python src/md2pdf.py <입력.md> <출력.pdf> [폰트폴더] [PDF 제목]")
    sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]

# 폰트 폴더: 주지 않으면 이 스크립트 위치 기준 ../data/font
if len(sys.argv) > 3:
    fontdir = sys.argv[3]
else:
    fontdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "font")

# 마크다운 파일 읽기
with open(src, encoding="utf-8") as f:
    markdown_text = f.read()

# PDF 제목: 주지 않으면 첫 번째 '# ' 로 시작하는 줄을 쓴다
title = ""
if len(sys.argv) > 4:
    title = sys.argv[4]
else:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

app = QApplication([])

# 폰트 폴더 안의 글꼴 파일을 Qt 에 등록한다
for name in os.listdir(fontdir):
    QFontDatabase.addApplicationFont(os.path.join(fontdir, name))

# 1) 마크다운 -> HTML (Qt 내장 변환기)
doc = QTextDocument()
doc.setMarkdown(markdown_text)
html = doc.toHtml()

# 2) Qt 가 넣은 글꼴 지정을 지우고 나눔 글꼴과 스타일을 입힌다
html = re.sub(r"font-family:'[^']*';", "", html)
css = """
body { font-family: 'NanumGothic'; font-size: 10pt; color: #222; }
h1 { font-size: 20pt; color: #1a3d6d; }
h2 { font-size: 14pt; color: #1a3d6d; margin-top: 16px; }
h3 { font-size: 11.5pt; color: #333; }
pre { font-family: 'NanumGothicCoding'; font-size: 8.5pt; background-color: #f3f4f6; }
code { font-family: 'NanumGothicCoding'; }
table { border-collapse: collapse; }
th { background-color: #e6ecf5; }
td, th { padding: 4px; }
"""
html = html.replace("<head>", "<head><style>" + css + "</style>", 1)
# 코드(고정폭) 부분은 나눔고딕코딩으로 바꾼다
html = re.sub(r"font-family:'?monospace'?", "font-family:'NanumGothicCoding'", html)
# 코드 블록 배경색, 표 테두리 색 지정
html = html.replace("<pre", "<pre bgcolor=\"#f3f4f6\"")
html = re.sub(r'<table border="1"', '<table border="1" bordercolor="#b0b8c4"', html)

out = QTextDocument()
out.setDefaultFont(QFont("NanumGothic", 10))
out.setDefaultStyleSheet(css)
out.setHtml(html)

# 3) A4, 여백 18mm 로 PDF 저장
writer = QPdfWriter(dst)
writer.setPageSize(QPageSize(QPageSize.A4))
writer.setPageMargins(QMarginsF(18, 18, 18, 18), QPageLayout.Millimeter)
writer.setResolution(300)
writer.setTitle(title)
out.print_(writer)

print("PDF 저장:", dst)
