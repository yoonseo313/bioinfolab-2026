# FASTQ 파일의 위치별(1번째 염기, 2번째 염기, ...) 평균 품질 점수를 계산하는 스크립트
# 사용법: python3 src/qual_by_position.py <FASTQ 파일>
# 출력: 위치<TAB>평균품질  (위치는 1부터 센다)
#
# read 마다 길이가 다를 수 있으므로(트리밍한 파일 등),
# 위치마다 "품질 점수 합계" 와 "그 위치를 가진 read 수" 를 따로 센다.
# 그래서 평균 = 그 위치의 점수 합계 / 그 위치를 가진 read 수 가 된다.
# 품질 점수는 Phred+33 인코딩으로 계산한다 (Q = ASCII 코드 - 33).

import sys


def qual_by_position(filename):
    """FASTQ 파일을 읽어 (위치별 점수 합계 리스트, 위치별 read 수 리스트)를 돌려준다."""
    sums = []    # sums[i]   = i번째 위치(0부터) 품질 점수의 합
    counts = []  # counts[i] = i번째 위치를 가진 read 의 수

    with open(filename) as f:
        line_number = 0
        for line in f:
            line_number = line_number + 1
            # FASTQ 는 4줄이 한 read 이고, 4번째 줄이 품질 문자열이다
            if line_number % 4 != 0:
                continue

            qual = line.rstrip()
            for i in range(len(qual)):
                score = ord(qual[i]) - 33
                # 지금까지 본 read 보다 긴 read 이면 리스트를 늘린다
                if i >= len(sums):
                    sums.append(0)
                    counts.append(0)
                sums[i] = sums[i] + score
                counts[i] = counts[i] + 1

    return sums, counts


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 src/qual_by_position.py <FASTQ 파일>")
        sys.exit(1)

    sums, counts = qual_by_position(sys.argv[1])

    print("위치\t평균품질")
    for i in range(len(sums)):
        average = sums[i] / counts[i]
        # 위치는 사람이 읽기 쉽게 1부터 센다
        print(f"{i + 1}\t{average:.2f}")


if __name__ == "__main__":
    main()
