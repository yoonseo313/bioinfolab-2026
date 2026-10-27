## 파이썬 치트시트

### 1. def 로 함수 만드는 모양

```python
def 함수이름(받을값1, 받을값2):
    """이 함수가 하는 일을 한 줄로."""
    결과 = 받을값1 + 받을값2
    return 결과
```

- `def` 줄 끝에 `:`, 그 아래 몸통은 모두 4칸 들여쓰기.
- 만들기만 하면 아무 일도 안 일어난다. `함수이름(1, 2)`처럼 불러야 실행된다.
- 함수는 그 함수를 부르는 코드보다 **위에** 있어야 한다.

### 2. print 와 return 의 차이

`print`는 화면에 보여 주기만 하고 끝, `return`은 값을 함수를 부른 쪽에 돌려줘서 변수에 담거나 다른 계산에 쓸 수 있다.

```python
x = gc_content("ATGC")   # return 이라서 x 에 0.5 가 들어간다
                         # print 였다면 0.5 가 화면에 찍히고 x 는 None
```

### 3. from 모듈 import 함수

```python
from fasta import read_fasta, gc_content   # fasta.py 에서 두 함수만 가져오기
seqs = read_fasta("data/a.fasta")          # 바로 이름으로 쓴다

import fasta                               # 모듈 통째로 가져오기
seqs = fasta.read_fasta("data/a.fasta")    # 이때는 "모듈이름." 을 앞에 붙인다
```

- 모듈 이름에는 `.py`를 붙이지 않는다 (`fasta.py` → `fasta`).
- 실행하는 스크립트와 같은 폴더에 있는 `.py` 파일은 바로 불러올 수 있다.

### 4. if __name__ == "__main__": 을 언제 쓰나

```python
def gc_content(seq):
    ...

if __name__ == "__main__":
    # 이 파일을 직접 실행할 때만 돈다
    print(gc_content("ATGC"))
```

| 실행 방법 | 아래 코드 실행? |
|---|---|
| `python3 src/fasta.py` (직접 실행) | 실행됨 |
| 다른 파일에서 `from fasta import ...` | 실행 안 됨 |

**언제?** 함수 모음 파일(모듈)에 시험 코드나 간단한 사용 예를 넣고 싶을 때.
이게 없으면 `import`할 때마다 시험 코드가 같이 돌아서 `sys.argv[1]` 에러 같은 게 난다.

### 5. 파일 열기 "w" 와 "a"

| 파이썬 | 뜻 | 파일이 이미 있으면 | bash 에서 같은 기호 |
|---|---|---|---|
| `open(파일, "w")` | write (쓰기) | 내용을 **지우고** 새로 씀 | `>` |
| `open(파일, "a")` | append (덧붙이기) | 기존 내용 **뒤에** 이어 씀 | `>>` |
| `open(파일)` | 읽기 (`"r"`이 기본값) | — | `<` |

```bash
echo "hello" > out.txt    # 덮어쓰기   = "w"
echo "world" >> out.txt   # 이어 쓰기  = "a"
```

- 같은 스크립트를 두 번 돌렸을 때 `"w"`는 결과가 같고, `"a"`는 내용이 두 배로 쌓인다.
- 반복문 안에서 `"w"`로 열면 매번 지워져서 마지막 내용만 남는다 → 파일은 반복문 **밖**에서 연다.

### 6. 발생한 오류 2가지
- cp 로 옮길때 lab07로 복붙할거라면 현재 위치가 lab07인지 살피고 할것! 홈으로 들어가서 냅다 하면 오류뜸
- print 이후에 type error - print는 값을 화면에 보여주기만 하고 끝나면 함수밖으로는 none이 나가는걸 기억