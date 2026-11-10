# paired-end FASTQ 두 파일(_1, _2)이 제대로 짝을 이루는지 확인하는 스크립트
# 사용법: python3 src/check_paired.py <_1.fastq> <_2.fastq>
#
# 확인하는 것
#   1. 두 파일의 read 개수가 같은가?
#   2. 같은 순서(n번째)에 있는 read 끼리 이름이 짝을 이루는가?
#      - 이름은 '@' 뒤 첫 단어(공백 앞)만 쓴다.
#        예) "@SRR1553607.1 1 length=101" -> "SRR1553607.1"
#      - 끝에 붙은 짝 표시("/1", "/2", ".1", ".2", "_1", "_2")는 떼고 비교한다.
#        예) "read7/1" 과 "read7/2" -> 둘 다 "read7" 이므로 짝이 맞다.
#
# 두 파일을 한꺼번에 메모리에 올리지 않고, 4줄(read 1개)씩 나란히 읽어 나간다.

import sys

# 화면에 보여 줄 "짝이 안 맞는 read" 의 최대 개수
MAX_SHOW = 5


def read_one_record(f):
    """파일에서 read 1개(4줄)를 읽어 이름을 돌려준다. 파일이 끝났으면 None."""
    header = f.readline()
    if header == "":
        return None          # 더 읽을 read 가 없다
    f.readline()             # 서열 줄 (여기서는 쓰지 않는다)
    f.readline()             # '+' 줄
    f.readline()             # 품질 줄
    return header.rstrip()[1:]   # 맨 앞의 '@' 를 뗀다


def base_name(name):
    """이름에서 첫 단어만 남기고, 끝의 짝 표시(/1, .2 등)를 뗀다."""
    first_word = name.split()[0]
    # 끝에서 두 번째 글자가 구분 기호이고 마지막 글자가 1 또는 2 이면 뗀다
    if len(first_word) >= 2 and first_word[-2] in "/._" and first_word[-1] in "12":
        return first_word[:-2]
    return first_word


def main():
    if len(sys.argv) != 3:
        print("사용법: python3 src/check_paired.py <_1.fastq> <_2.fastq>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    count1 = 0          # 파일 1의 read 개수
    count2 = 0          # 파일 2의 read 개수
    mismatch = 0        # 이름이 짝을 이루지 않는 read 쌍의 개수
    examples = []       # 짝이 안 맞는 예 (몇 개만 모아 둔다)

    with open(file1) as f1, open(file2) as f2:
        while True:
            name1 = read_one_record(f1)
            name2 = read_one_record(f2)

            # 두 파일 모두 끝났으면 멈춘다
            if name1 is None and name2 is None:
                break

            if name1 is not None:
                count1 = count1 + 1
            if name2 is not None:
                count2 = count2 + 1

            # 한쪽만 끝났으면 이름 비교는 할 수 없으므로 개수만 계속 센다
            if name1 is None or name2 is None:
                continue

            # 같은 순서의 두 read 이름을 비교한다
            if base_name(name1) != base_name(name2):
                mismatch = mismatch + 1
                if len(examples) < MAX_SHOW:
                    examples.append((count1, name1, name2))

    # 결과 출력
    print("파일 1:", file1, "-> read", count1, "개")
    print("파일 2:", file2, "-> read", count2, "개")

    if count1 == count2:
        print("[통과] 두 파일의 read 개수가 같다.")
    else:
        print("[실패] 두 파일의 read 개수가 다르다. (차이:", abs(count1 - count2), "개)")

    compared = min(count1, count2)
    if mismatch == 0:
        print("[통과] 비교한", compared, "쌍 모두 이름이 짝을 이룬다.")
    else:
        print("[실패] 비교한", compared, "쌍 중", mismatch, "쌍의 이름이 짝을 이루지 않는다.")
        print("  짝이 안 맞는 예 (순서, 파일1 이름, 파일2 이름):")
        for number, n1, n2 in examples:
            print("   ", number, "|", n1, "|", n2)


if __name__ == "__main__":
    main()
