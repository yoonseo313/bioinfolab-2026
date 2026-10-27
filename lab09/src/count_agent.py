"""FASTA 파일 이름을 받아 서열 개수를 출력한다."""
import sys


def count_seqs(filename):
    """FASTA 파일에서 '>'로 시작하는 줄(서열 헤더)의 개수를 센다."""
    count = 0
    with open(filename) as f:
        for line in f:
            if line.startswith(">"):
                count = count + 1
    return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python count_agent.py <FASTA 파일>")
        sys.exit(1)
    print(count_seqs(sys.argv[1]))
