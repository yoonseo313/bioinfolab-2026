"""폴더 안 모든 FASTA 파일의 요약 정보를 TSV 파일로 저장한다."""
import sys  #명령줄에 입력한 단어들 (sys.argv)쓰기위해 불러옴
import glob #.fasta와 같은패턴으로 파일목록 찾는기능
from fasta import read_fasta, gc_content, length_stats
#우리가 만든 fasta.py에서 함수 3개 가져옴

folder = sys.argv[1]
outfile = sys.argv[2]
#[1]-"data"(읽을폴더),[2]-"results.tsv"(저장할 파일)

with open(outfile, "w") as out: #결과파일을 쓰기모드"w"로 열어, 파일이 없으면 만들고 있으면 지우고 새로쓰기, 열린파일을 out이라고 쓰기
    out.write("file\tcount\ttotal\tmean_gc\n") #머리줄, \t는 탭, \n은 줄바꿈
    for path in sorted(glob.glob(folder + "/*.fasta")): 
        seqs = read_fasta(path)
        stats = length_stats(seqs)

        gc_values = []
        for name in seqs:
            gc_values.append(gc_content(seqs[name]))
        if len(gc_values) == 0:
            mean_gc = 0.0
        else:
            mean_gc = sum(gc_values) / len(gc_values)

        out.write(f"{path}\t{stats['count']}\t{stats['total']}\t{mean_gc:.3f}\n")

print(outfile, "에 저장했습니다.")