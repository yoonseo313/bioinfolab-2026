# FASTQ 파일의 각 read 에 대해 GC 비율과 평균 품질을 함께 계산하는 스크립트
#
# 사용법: python3 src/gc_content.py <FASTQ 파일> [극단 비율(%)]
#   예) python3 src/gc_content.py data/SRR1553607_1.fastq > doc/gc_quality.tsv
#
# 출력은 두 부분으로 나뉜다.
#   1) read 별 결과 표  -> 표준 출력(stdout)
#      이름<TAB>길이<TAB>GC(%)<TAB>평균품질
#      '>' 로 파일에 저장할 수 있다.
#   2) 요약 비교       -> 표준 에러(stderr)
#      '>' 로 저장해도 화면에 그대로 보인다.
#      GC 비율이 가장 낮은 read 들(하위 N%)과 가장 높은 read 들(상위 N%)을 골라
#      그 평균 품질을 전체 평균 품질과 비교한다. N 의 기본값은 5 이다.
#
# GC 비율은 lab07/src/fasta.py 의 gc_content 함수로 계산한다.
# 품질 점수는 Phred+33 인코딩으로 계산한다 (Q = ASCII 코드 - 33).

import os
import sys

# lab07/src 폴더를 모듈 검색 경로에 넣어야 fasta.py 를 불러올 수 있다
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "..", "..", "lab07", "src"))
from fasta import gc_content


def mean_quality(qual):
    """품질 문자열의 평균 Phred 점수를 돌려준다."""
    total = 0
    for ch in qual:
        total = total + (ord(ch) - 33)
    return total / len(qual)


def average(numbers):
    """숫자 리스트의 평균을 돌려준다."""
    return sum(numbers) / len(numbers)


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 src/gc_content.py <FASTQ 파일> [극단 비율(%)]")
        sys.exit(1)

    filename = sys.argv[1]
    # 극단으로 볼 비율(%) : 하위 N%, 상위 N%
    if len(sys.argv) > 2:
        percent = float(sys.argv[2])
    else:
        percent = 5.0

    results = []  # (GC(%), 평균품질) 을 read 마다 모아 둔다 (요약 비교에 사용)

    print("이름\t길이\tGC(%)\t평균품질")

    with open(filename) as f:
        line_number = 0
        name = ""
        seq = ""
        for line in f:
            line_number = line_number + 1
            line = line.rstrip()
            # FASTQ 는 4줄이 한 read: 1 이름, 2 서열, 3 '+', 4 품질
            if line_number % 4 == 1:
                name = line[1:].split()[0]  # '@' 를 떼고 첫 단어만 이름으로 쓴다
            elif line_number % 4 == 2:
                seq = line.upper()
            elif line_number % 4 == 0:
                qual = line
                if len(seq) == 0:
                    continue  # 길이가 0인 read 는 건너뛴다 (0으로 나누기 방지)
                gc = gc_content(seq) * 100
                q = mean_quality(qual)
                results.append((gc, q))
                print(f"{name}\t{len(seq)}\t{gc:.2f}\t{q:.2f}")

    if len(results) == 0:
        print("read 가 없습니다.", file=sys.stderr)
        sys.exit(1)

    # ---- 요약 비교: GC 극단 read 의 품질 vs 전체 ----
    # GC 비율 순서로 정렬한 뒤 앞쪽 N% 를 '낮은 GC', 뒤쪽 N% 를 '높은 GC' 로 본다
    results.sort()
    n = int(len(results) * percent / 100)
    if n == 0:
        n = 1
    low = results[:n]
    high = results[-n:]

    all_gc = []
    all_q = []
    for gc, q in results:
        all_gc.append(gc)
        all_q.append(q)
    low_q = []
    for gc, q in low:
        low_q.append(q)
    high_q = []
    for gc, q in high:
        high_q.append(q)

    total_avg = average(all_q)
    low_avg = average(low_q)
    high_avg = average(high_q)

    # 요약은 표준 에러로 출력한다 (표를 파일로 저장해도 화면에 보이도록)
    out = sys.stderr
    print("", file=out)
    print("===== GC 비율 극단 read 의 평균 품질 비교 =====", file=out)
    print(f"전체 read 수: {len(results)}", file=out)
    print(f"전체 평균 GC(%): {average(all_gc):.2f}", file=out)
    print(f"전체 평균 품질: {total_avg:.2f}", file=out)
    print("", file=out)
    print("구분\tread 수\tGC 범위(%)\t평균품질\t전체와 차이", file=out)
    print(f"GC 하위 {percent:g}%\t{len(low)}\t{low[0][0]:.2f}~{low[-1][0]:.2f}\t"
          f"{low_avg:.2f}\t{low_avg - total_avg:+.2f}", file=out)
    print(f"GC 상위 {percent:g}%\t{len(high)}\t{high[0][0]:.2f}~{high[-1][0]:.2f}\t"
          f"{high_avg:.2f}\t{high_avg - total_avg:+.2f}", file=out)


if __name__ == "__main__":
    main()
