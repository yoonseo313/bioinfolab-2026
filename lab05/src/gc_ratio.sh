#!/usr/bin/bash
# gc_ratio.sh — 서열의 GC 비율을 소수점 넷째 자리까지 출력한다
# 사용법: gc_ratio.sh [서열]   (인자가 없으면 예시 서열을 사용한다)

SEQ="$1"
if [ -z "$SEQ" ]
then
    SEQ="ATGCGATACGCTTGA"
fi

LEN=${#SEQ}
GC=$(echo "$SEQ" | grep -o "[GC]" | wc -l)

echo "서열: $SEQ"
echo "길이: $LEN, GC 개수: $GC"

# 시도 1: 산술 확장으로 그냥 나누기 → 정수만 남는다
echo "시도 1 (그냥 나누기): $(( GC / LEN ))"

# 시도 2: 산술 확장만으로 우회하기
#   10000 을 먼저 곱하고 나누면 소수 넷째 자리까지를 정수로 얻는다 (7*10000/15 = 4666)
R=$(( GC * 10000 / LEN ))
INT=$(( R / 10000 ))                   # 정수 부분
FRAC=$(( R % 10000 + 10000 ))          # 소수 부분, 앞자리 0 을 지키려고 10000 을 더함
FRAC=$(echo "$FRAC" | cut -c2-5)       # 맨 앞의 1 을 잘라 내고 네 자리만 남김
echo "시도 2 (산술 확장 우회): $INT.$FRAC"

# 시도 3: bc 로 소수 계산하기
echo "시도 3 (bc): $(echo "scale=4; $GC / $LEN" | bc)"