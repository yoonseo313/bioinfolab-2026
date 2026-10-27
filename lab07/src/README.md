# fasta.py 도구 상자

FASTA 파일을 읽고, 쓰고, 서열을 간단히 분석하는 함수 모음이다.
다른 스크립트에서 아래처럼 불러와 쓴다 (`fasta.py`와 같은 `src` 폴더 안에서).

```python
from fasta import read_fasta, write_fasta, gc_content, reverse_complement, length_stats
```

`fasta.py`를 직접 실행하면 간단한 시험을 해 볼 수 있다.

```bash
python3 src/fasta.py data/sample.fasta
```

## 함수 목록

| 함수 | 받는 것 | 돌려주는 것 |
|---|---|---|
| `read_fasta(filename)` | FASTA 파일 경로 | `{서열이름: 서열}` 딕셔너리 |
| `write_fasta(seqs, filename)` | `{서열이름: 서열}` 딕셔너리, 저장할 파일 경로 | 없음 (파일을 만든다) |
| `gc_content(seq)` | 서열 문자열 하나 | G와 C가 차지하는 비율 (0~1 사이 실수) |
| `reverse_complement(seq)` | 서열 문자열 하나 | 반대쪽 가닥을 읽는 방향대로 쓴 서열 |
| `length_stats(seqs)` | `{서열이름: 서열}` 딕셔너리 | 개수·전체 길이·평균·최소·최대 길이를 담은 딕셔너리 |

## 함수별 설명과 사용 예

### read_fasta(filename)
FASTA 파일을 열어서 서열마다 이름을 열쇠로, 서열을 값으로 하는 딕셔너리를 만든다.
`>` 줄에서 첫 번째 띄어쓰기 앞까지만 이름으로 쓰고, 여러 줄에 나뉜 서열은 한 줄로 이어 붙이며 모두 대문자로 바꾼다.

```python
seqs = read_fasta("data/sample.fasta")   # {"seq1": "ATGC...", "seq2": "GGTA..."}
```

### write_fasta(seqs, filename)
`read_fasta`와 반대로, 딕셔너리를 FASTA 형식 파일로 저장한다. 서열 하나는 줄바꿈 없이 한 줄로 쓴다.
같은 이름의 파일이 있으면 덮어쓰므로 주의.

```python
write_fasta({"my_seq": "ATGCGT"}, "out.fasta")
```

### gc_content(seq)
서열에서 G와 C가 몇 퍼센트인지를 0과 1 사이 숫자로 알려 준다. 빈 서열이면 0.0.
퍼센트로 보고 싶으면 100을 곱한다.

```python
gc_content("ATGC")   # 0.5
```

### reverse_complement(seq)
DNA의 반대쪽 가닥 서열을 구한다. A↔T, G↔C로 바꾼 다음 순서를 뒤집는다.
두 번 적용하면 원래 서열로 돌아온다.

```python
reverse_complement("ATGC")   # "GCAT"
```

### length_stats(seqs)
파일 전체에 서열이 몇 개 있고 길이가 어느 정도인지 한눈에 보는 요약표를 만든다.
값은 `"count"`, `"total"`, `"mean"`, `"min"`, `"max"`라는 이름으로 꺼낸다. 서열이 없으면 모두 0.

```python
stats = length_stats(read_fasta("data/sample.fasta"))   # stats["mean"] 으로 평균 길이
```

## 이 도구를 쓰는 스크립트

- `stats.py` : FASTA 파일 하나의 길이 통계를 화면에 출력
  `python3 src/stats.py data/sample.fasta`
- `batchinfo.py` : 폴더 안 모든 `.fasta` 파일의 개수·길이·평균 GC를 TSV로 저장
  `python3 src/batchinfo.py data results.tsv`

## 아직 부족한 점

- `read_fasta`: 첫 줄이 `>`로 시작하지 않는 파일이면 이름이 없는 상태에서 서열을 붙이려다 에러가 난다.
  또 같은 이름의 서열이 두 번 나오면 뒤의 것이 앞의 것을 조용히 덮어쓴다.
- `read_fasta`: `>` 줄의 첫 단어 뒤에 있는 설명(유전자 이름, 생물종 등)이 버려진다.
- `write_fasta`: 서열을 한 줄로만 쓴다. 보통 FASTA 파일처럼 60~70글자마다 줄을 바꿔 주면 좋겠다.
- `reverse_complement`: A, T, G, C 말고 `N` 같은 글자가 있으면 `KeyError`가 난다.
  소문자를 직접 넣어도 마찬가지다 (`read_fasta`로 읽은 서열은 대문자라 괜찮다).
- `gc_content`: `N`도 길이에 포함되므로 `N`이 많은 서열은 GC 비율이 실제보다 낮게 나온다.

## 추가하고 싶은 함수

- `count_bases(seq)` : A, T, G, C, N이 각각 몇 개인지 딕셔너리로 돌려주기
- `filter_by_length(seqs, min_len)` : 일정 길이보다 짧은 서열을 빼고 돌려주기
- `translate(seq)` : DNA 서열을 아미노산 서열로 번역하기
- `n50(seqs)` : 조립 결과를 평가할 때 쓰는 N50 값 구하기