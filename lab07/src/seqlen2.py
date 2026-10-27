import sys
from fasta import read_fasta

seqs = read_fasta(sys.argv[1])
for name in seqs:
    print(name, len(seqs[name]))
