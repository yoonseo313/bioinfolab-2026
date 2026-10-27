"""FASTA 파일의 서열 길이 통계를 출력한다."""
import sys
from fasta import read_fasta, length_stats  #같은 src 폴더에 있는 fasta.py에서 함수 불러옴

filename = sys.argv[1]
seqs = read_fasta(filename)
stats = length_stats(seqs)

print("파일:", filename)
print("-" * 30)
print(f"서열 개수   : {stats['count']}")
print(f"전체 길이   : {stats['total']}")
print(f"평균 길이   : {stats['mean']:.1f}")
print(f"가장 짧은 것: {stats['min']}")
print(f"가장 긴 것  : {stats['max']}")

# 이때 fasta.py의 if__name__=="__main__":은 실행되지 않음, 직접 실행시에만 돌고, 다른파일에서 import 시 함수정의만 가져옴