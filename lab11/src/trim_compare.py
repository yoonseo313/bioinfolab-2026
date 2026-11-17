import sys

# 사용법: python3 src/trim_compare.py <FASTQ 파일1> <FASTQ 파일2> ...
# 여러 FASTQ 파일의 read 개수, 평균 길이, 전체 평균 품질,
# 가장 짧은 read 길이, 가장 긴 read 길이를 표(마크다운)로 출력한다.


def fastq_stats(filename):
    count = 0          # read 개수
    total_len = 0      # 모든 read 길이의 합
    total_qual = 0     # read 별 평균 품질의 합
    min_len = None     # 가장 짧은 read 길이
    max_len = None     # 가장 긴 read 길이

    with open(filename) as f:
        line_no = 0
        for line in f:
            line_no = line_no + 1
            # FASTQ 는 4줄이 한 묶음: 1 이름, 2 서열, 3 '+', 4 품질
            if line_no % 4 == 2:
                seq = line.rstrip()
            elif line_no % 4 == 0:
                qual = line.rstrip()
                length = len(seq)

                count = count + 1
                total_len = total_len + length

                # 최소/최대 길이 갱신
                if min_len is None or length < min_len:
                    min_len = length
                if max_len is None or length > max_len:
                    max_len = length

                # 품질 문자 -> Phred 점수 (ASCII - 33), read 하나의 평균
                score_sum = 0
                for ch in qual:
                    score_sum = score_sum + (ord(ch) - 33)
                total_qual = total_qual + score_sum / length

    mean_len = total_len / count
    mean_qual = total_qual / count   # qual_summary.py 와 같은 방식(read 평균들의 평균)
    return count, mean_len, mean_qual, min_len, max_len


print("| 파일 | read 개수 | 평균 길이 | 전체 평균 품질 | 최소 길이 | 최대 길이 |")
print("|---|---:|---:|---:|---:|---:|")
for filename in sys.argv[1:]:
    count, mean_len, mean_qual, min_len, max_len = fastq_stats(filename)
    print(f"| {filename} | {count:,} | {mean_len:.2f} | {mean_qual:.2f} | {min_len} | {max_len} |")
