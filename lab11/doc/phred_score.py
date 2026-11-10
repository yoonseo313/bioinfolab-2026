# FASTQ 품질 문자열의 각 위치별 품질 점수(Phred)와 전체 평균을 계산하는 스크립트
# 사용법: python3 doc/phred_score.py [품질문자열]
#   품질 문자열을 주지 않으면 예제 문자열 "IIIIIIII#####IIIIIIIIII" 을 사용한다.
#
# Phred+33 인코딩 (Illumina 1.8 이상, 현재 대부분의 FASTQ 형식):
#   품질 점수 Q = 문자의 ASCII 코드 - 33
#   예) 'I' = 73 -> Q = 40,  '#' = 35 -> Q = 2
#   Q 가 클수록 그 염기를 잘못 읽었을 확률(P = 10^(-Q/10))이 작다.

import sys


def phred_scores(quality):
    """품질 문자열을 받아 각 위치의 Phred 점수 리스트를 돌려준다."""
    scores = []
    for ch in quality:
        q = ord(ch) - 33  # ord() 는 문자의 ASCII 코드를 돌려준다
        scores.append(q)
    return scores


def main():
    # 명령줄 인자가 있으면 그것을, 없으면 예제 문자열을 사용한다
    if len(sys.argv) > 1:
        quality = sys.argv[1]
    else:
        quality = "IIIIIIII#####IIIIIIIIII"

    scores = phred_scores(quality)

    print("품질 문자열:", quality)
    print("길이:", len(quality))
    print()
    print("위치\t문자\tASCII\tQ\t오류확률")
    for i in range(len(quality)):
        ch = quality[i]
        q = scores[i]
        error_prob = 10 ** (-q / 10)  # Q 점수를 오류 확률로 바꾼다
        # 위치는 사람이 읽기 쉽게 1부터 센다
        print(f"{i + 1}\t{ch}\t{ord(ch)}\t{q}\t{error_prob:.4f}")

    # 전체 평균 품질 점수
    average = sum(scores) / len(scores)
    print()
    print("점수 합계:", sum(scores))
    print(f"평균 품질 점수: {average:.2f}")


if __name__ == "__main__":
    main()
