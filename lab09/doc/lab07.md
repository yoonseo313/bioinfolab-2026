# lab07 요약: 함수와 모듈로 FASTA 도구 만들기

lab07에서는 반복해서 쓰던 FASTA 처리 코드를 **함수**로 만들고, 이를 `fasta.py`라는 **모듈**에 모아 여러 스크립트에서 `import`해 쓰는 방법을 익혔다.

## 1. 폴더 구조

```
lab07/
├── data/          # 입력 FASTA (seqs.fasta, seqs2.fasta, lower.fasta)
├── doc/           # 결과물 (summary.tsv, long.fasta)
├── src/           # 스크립트, fasta.py 모듈, README.md, py_cheatsheet.md
└── results.tsv    # batchinfo2.py 실행 결과
```

## 2. 함수 기초

| 파일 | 내용 |
|---|---|
| `fgc.py` | `def`로 `gc_content(seq)` 함수를 정의하고 호출 |
| `fseqlen.py` | `print`와 `return`의 차이 확인. `print`만 하는 함수의 결과는 `None` |
| `filter.py` | 함수 없이 FASTA를 읽은 뒤 길이 20~40, GC 0.4~0.6, N 5개 미만인 서열만 출력 (함수로 정리하기 전 버전) |

- 함수는 정의만 해서는 실행되지 않고, 호출해야 실행된다.
- `return`으로 돌려받은 값은 변수에 담거나 다른 계산에 이어서 쓸 수 있다.

## 3. `fasta.py` 모듈

| 함수 | 입력 | 출력 |
|---|---|---|
| `read_fasta(filename)` | FASTA 경로 | `{이름: 서열}` 딕셔너리 (대문자로 변환, 여러 줄 서열은 이어 붙임) |
| `write_fasta(seqs, filename)` | 딕셔너리, 저장 경로 | FASTA 파일 생성 (`"w"` 모드라 덮어씀) |
| `gc_content(seq)` | 서열 | GC 비율 (0~1). 빈 서열이면 0.0 |
| `reverse_complement(seq)` | 서열 | 역상보 서열 (`ATGC` → `GCAT`) |
| `length_stats(seqs)` | 딕셔너리 | `count`, `total`, `mean`, `min`, `max` |

`if __name__ == "__main__":` 블록에 시험 코드를 넣었다. 이 블록은 `python3 src/fasta.py data/seqs.fasta`처럼 직접 실행할 때만 돌고, 다른 파일에서 `import`할 때는 실행되지 않는다. 역상보를 두 번 적용하면 원래 서열이 되는지 `assert`로 확인한다.

## 4. 모듈을 활용한 스크립트

| 스크립트 | 사용법 | 하는 일 |
|---|---|---|
| `countseq2.py` | `python3 src/countseq2.py data/seqs.fasta` | 서열 개수 출력 |
| `seqlen2.py` | `python3 src/seqlen2.py data/seqs.fasta` | 서열별 이름과 길이 출력 |
| `stats.py` | `python3 src/stats.py data/seqs.fasta` | 개수, 전체/평균/최소/최대 길이 출력 |
| `summary.py` | `python3 src/summary.py data/seqs.fasta doc/summary.tsv` | 서열별 이름, 길이, GC를 TSV로 저장 |
| `filter_fasta.py` | `python3 src/filter_fasta.py <입력> <최소길이> <출력>` | 최소 길이 이상인 서열만 새 FASTA로 저장 |
| `batchinfo2.py` | `python3 src/batchinfo2.py data results.tsv` | `glob`으로 폴더 안 모든 `.fasta`를 찾아 파일별 개수, 전체 길이, 평균 GC를 TSV로 저장 |

## 5. 실행 결과

**`doc/summary.tsv`** (seqs.fasta 서열별 요약)

| name | length | gc |
|---|---|---|
| gene1 | 30 | 0.5 |
| gene2 | 15 | 0.4667 |
| gene3 | 22 | 0.5455 |

**`doc/long.fasta`**: 길이 20 이상인 gene1(30), gene3(22)만 남았다.

**`results.tsv`** (data 폴더 일괄 요약)

| file | count | total | mean_gc |
|---|---|---|---|
| data/lower.fasta | 2 | 20 | 0.650 |
| data/seqs.fasta | 3 | 67 | 0.504 |
| data/seqs2.fasta | 2 | 16 | 0.250 |

`lower.fasta`는 소문자 서열이지만 `read_fasta`가 대문자로 바꾸기 때문에 GC가 제대로 계산된다.

## 6. 정리한 개념 (`py_cheatsheet.md`)

- **`def`**: 줄 끝에 `:`을 붙이고 몸통은 4칸 들여쓴다. 함수를 호출하는 코드보다 위에 정의해야 한다.
- **`print`와 `return`**: `print`는 화면에 보여 주기만 하고, `return`은 값을 호출한 쪽으로 돌려준다.
- **`from 모듈 import 함수`**: 모듈 이름에는 `.py`를 쓰지 않는다. `import fasta`로 가져오면 `fasta.read_fasta()`처럼 모듈 이름을 앞에 붙인다.
- **`if __name__ == "__main__":`**: 모듈 안에 넣은 시험 코드가 import할 때 실행되지 않게 막는다.
- **파일 모드**: `"w"`는 덮어쓰기(bash의 `>`), `"a"`는 이어쓰기(`>>`), 기본값은 읽기(`"r"`). 반복문 안에서 `"w"`로 열면 마지막 내용만 남으므로 파일은 반복문 밖에서 연다.

## 7. 겪은 오류

- `cp`로 파일을 복사할 때 현재 위치를 확인하지 않아 경로 오류가 났다.
- `print`만 하는 함수의 결과(`None`)로 계산을 하려다 `TypeError`가 났다.

## 8. 남은 개선점 (`src/README.md`)

- `read_fasta`: 첫 줄이 `>`로 시작하지 않으면 에러가 난다. 같은 이름이 두 번 나오면 뒤의 서열이 앞의 것을 덮어쓰고, 헤더의 설명 부분은 버려진다.
- `write_fasta`: 서열을 한 줄로만 쓴다. 60~70글자마다 줄을 바꾸면 좋겠다.
- `reverse_complement`: `N`이나 소문자가 들어오면 `KeyError`가 난다.
- `gc_content`: `N`도 길이에 포함돼 GC 비율이 실제보다 낮게 나온다.
- `filter_fasta.py`: `minlen = sys.argv[2]`가 문자열이라 `len(...) >= minlen` 비교에서 `TypeError`가 난다. `int(sys.argv[2])`로 바꿔야 한다.
- 추가하고 싶은 함수: `count_bases`, `filter_by_length`, `translate`, `n50`
