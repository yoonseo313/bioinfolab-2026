"""FASTA 파일 이름을 받아 서열 개수를 출력한다."""
import os
import sys

# lab07/src 폴더를 찾아 sys.path 에 넣어야 fasta.py 를 불러올 수 있다
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "..", "..", "lab07", "src"))

from fasta import read_fasta


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 count_agent2.py <FASTA 파일>")
        sys.exit(1)

    # read_fasta 는 {이름: 서열} 딕셔너리를 돌려주므로 그 길이가 서열 개수이다
    # (주의: 이름이 겹치는 서열은 덮어써져서 하나로 세어진다)
    seqs = read_fasta(sys.argv[1])
    print(len(seqs))
