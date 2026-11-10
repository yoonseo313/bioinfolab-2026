# parse_fastq.py 사용 설명서

## 1. 개요

`src/parse_fastq.py` 는 FASTQ 파일을 읽어서 다음 네 가지를 화면에 출력하는 스크립트이다.

- 전체 read 개수
- 첫 번째 read 의 이름
- 첫 번째 read 의 서열
- 첫 번째 read 의 길이

표준 라이브러리(`sys`)만 사용하므로 별도 설치 없이 실행된다.

## 2. 사용법

lab11 폴더 안에서 실행한다.

```bash
cd lab11
python3 src/parse_fastq.py <FASTQ 파일 경로>
```

### 실행 예시

```bash
python3 src/parse_fastq.py data/SRR1553607_1.fastq
```

출력 결과:

```
read 개수: 203445
첫 read 이름: SRR1553607.1 1 length=101
첫 read 서열: GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
첫 read 길이: 101
```

`data/SRR1553607_1.fastq` 는 813,780 줄이다. 한 read 가 4줄이므로 813,780 ÷ 4 = 203,445 개의 read 가 있다.

## 3. 입력 파일 형식 (FASTQ)

FASTQ 파일에서는 read 하나가 **정확히 4줄**이다.

```
@SRR1553607.1 1 length=101        ← 1줄: '@' 로 시작하는 이름 줄
GTTAGCGTTGTTGATCGCGACG...         ← 2줄: 염기 서열
+SRR1553607.1 1 length=101        ← 3줄: '+' 로 시작하는 구분선
BB@FFFFFHHHHHJJJJJJJJJ...         ← 4줄: 품질 점수 (서열과 길이가 같다)
```

## 4. 코드 설명

### 4.1 `read_fastq(filename)` 함수

```python
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()

    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))

    return records
```

| 코드 | 하는 일 |
|------|---------|
| `f.readlines()` | 파일의 모든 줄을 리스트로 한꺼번에 읽는다. |
| `range(0, len(lines), 4)` | `i` 를 0, 4, 8, … 처럼 4씩 늘린다. `i` 는 항상 각 read 의 첫 줄(이름 줄)을 가리킨다. |
| `lines[i].rstrip()[1:]` | 줄 끝의 줄바꿈(`\n`)을 지우고, 맨 앞의 `@` 를 뺀 나머지를 이름으로 쓴다. |
| `lines[i + 1].rstrip()` | 서열 줄이다. |
| `lines[i + 3].rstrip()` | 품질 점수 줄이다. 3번째 줄(`+`)인 `i + 2` 는 사용하지 않는다. |
| `records.append((name, seq, qual))` | read 하나를 `(이름, 서열, 품질)` 튜플로 묶어 리스트에 넣는다. |

**반환값**: `(이름, 서열, 품질)` 튜플의 리스트이다.

```python
[
    ("SRR1553607.1 1 length=101", "GTTAGC...", "BB@FFF..."),
    ("SRR1553607.2 2 length=101", "GGTGTA...", "?@;BDD..."),
    ...
]
```

### 4.2 메인 부분

```python
reads = read_fastq(sys.argv[1])
print("read 개수:", len(reads))
print("첫 read 이름:", reads[0][0])
print("첫 read 서열:", reads[0][1])
print("첫 read 길이:", len(reads[0][1]))
```

- `sys.argv[1]` 은 명령어 뒤에 적은 첫 번째 인자, 곧 FASTQ 파일 경로이다.
- `reads[0]` 은 첫 번째 read 이다. `[0]` 은 이름, `[1]` 은 서열, `[2]` 는 품질이다.

## 5. 주의할 점과 한계

| 상황 | 결과 |
|------|------|
| 파일 이름을 주지 않고 실행함 | `sys.argv[1]` 이 없어서 `IndexError` 가 난다. |
| 파일 줄 수가 4의 배수가 아님 (파일이 잘렸거나 끝에 빈 줄이 있음) | 마지막 반복에서 `lines[i + 1]` 등이 없어서 `IndexError` 가 난다. |
| 빈 파일 | `reads` 가 빈 리스트라서 `reads[0]` 에서 `IndexError` 가 난다. |
| 이름 줄이 `@` 로 시작하지 않음 | 검사하지 않으므로 첫 글자가 그냥 잘린다. 형식이 틀린 파일도 에러 없이 읽힌다. |
| 서열이 여러 줄로 나뉜 FASTQ | 4줄 형식만 처리하므로 잘못 읽는다. (요즘 시퀀서 출력은 대부분 4줄 형식이다.) |
| 매우 큰 파일 | `readlines()` 가 파일 전체를 메모리에 올린다. 이 실습 파일(약 20만 read)은 문제없지만, 수천만 read 짜리 파일에서는 메모리가 부족할 수 있다. |
| 압축 파일(`.fq.gz`) | `open()` 으로는 읽을 수 없다. 먼저 `gunzip` 으로 풀어야 한다. |

## 6. 더 해 볼 만한 것

- 3번째 줄이 `+` 로 시작하는지, 서열과 품질 길이가 같은지 검사하기
- 모든 read 의 평균 길이, 최소·최대 길이 구하기
- 품질 문자를 점수로 바꾸기: `ord(문자) - 33` (Phred+33)
- `readlines()` 대신 한 줄씩 읽어 메모리를 적게 쓰도록 바꾸기
