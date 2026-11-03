"""FASTA 파일을 다루는 함수 모음"""
 
 
def read_fasta(filename):
    """FASTA 파일을 읽어 {이름: 서열} 딕셔너리로 돌려준다."""
    seqs = {}
    name = None
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = ""
            else:
                seqs[name] = seqs[name] + line.upper()
    return seqs

def write_fasta(seqs, filename):
    """{이름: 서열} 딕셔너리를 FASTA 파일로 저장한다."""
    with open(filename, "w") as out:
        for name in seqs:
            out.write(">" + name + "\n")
            out.write(seqs[name] + "\n")

 
def gc_content(seq):
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다."""
    if len(seq) == 0:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)

def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다."""
    pairs = {"A": "T", "T": "A", "G": "C", "C": "G"}
    comp = ""
    for base in seq:
        comp = comp + pairs[base]
    return comp[::-1]

def length_stats(seqs):
    """{이름:서열} 딕셔너리를 받아 길이 통계를 딕셔너리로 돌려준다."""
    lengths = []   #각 서열의 길이를 모아둘 빈 리스트
    for name in seqs: #딕셔너리의 이름을 하나씩 꺼내 그 서열 길이를 리스트 끝에 붙임
        lengths.append(len(seqs[name]))

    if len(lengths) == 0:  #서열이 하나도 없을 때를 대비
        return {"count":0, "total":0, "mean":0.0, "min":0, "max":0}  

    total = sum(lengths)  #리스트 숫자를 모두 더함(전체길이)
    return {
        "count": len(lengths),
        "total": total,
        "mean":total/len(lengths),
        "min":min(lengths), #리스트의 가장 작은값을 돌려줌
        "max":max(lengths), #리스트의 가장 큰 값을 돌려줌
    }  # return 안의 값 5개를 이름표를 붙여 딕셔너리 하나로 돌려줌

if __name__ == "__main__":
    import sys
    seqs = read_fasta(sys.argv[1])
    for name in seqs:
        print(name, len(seqs[name]), round(gc_content(seqs[name]), 3))

    # reverse_complement 시험
    print(reverse_complement("ATGC"))          # GCAT 가 나와야 한다
    for name in seqs:
        seq = seqs[name]
        assert reverse_complement(reverse_complement(seq)) == seq
    print("reverse_complement 시험 통과")
