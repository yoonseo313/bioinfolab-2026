# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 이 저장소의 규칙

## 이 저장소는
생물정보학실험 수업의 실습 저장소이다. 주차별로 labNN 폴더가 있다.

- 새 주차 폴더는 `lab-template` 을 복사해 만든다 (`cp -r lab-template labNN`). 각 폴더는 `data/`(입력·내려받은 데이터), `doc/`(보고서·결과 요약), `src/`(직접 쓴 `.sh`, `.py`) 로 나뉜다.
- `resources/` 는 강의자가 준 예제 데이터(`resources/data/`)와 예제 스크립트(`resources/src/`)이다.
- 학생이 쓴 학습용 코드이므로 초보자가 읽기 쉬운 수준(표준 라이브러리, 단순한 반복문, 친절한 한국어 주석)을 유지한다. `bugN.py`/`bugN.sh` 는 일부러 버그를 넣은 디버깅 연습 파일이다.

## 실행 환경
- Codespaces devcontainer(`.devcontainer/1-basic` ~ `4-genome`)로 주차별 환경을 고른다. 1-basic 은 파이썬과 리눅스 기본 명령어만, 3-seq 는 seqkit·blast·mafft·iqtree·fastqc·fastp, 4-genome 은 여기에 shovill·prokka 가 더 있다. 지금 환경에 어떤 도구가 있는지는 `bash .devcontainer/check.sh` 로 확인한다.
- 필요한 도구가 없으면 설치하지 말고 사용자에게 알린다 (conda 실습 주차만 예외로 학생이 직접 설치한다).
- 빌드·린트·테스트 도구는 없다. 스크립트는 lab 폴더 안에서 `python3 src/<스크립트>.py data/<파일>.fasta` 처럼 실행해 확인한다.
- `fasta.py` 의 자체 시험: `cd lab07 && python3 src/fasta.py data/seqs.fasta` (`if __name__ == "__main__":` 블록의 assert 가 돈다).

## fasta.py 모듈
- `lab07/src/fasta.py` 에 `read_fasta`, `write_fasta`, `gc_content`, `reverse_complement`, `length_stats` 가 있다. 사용법과 알려진 한계는 `lab07/src/README.md` 에 정리되어 있다.
- lab07 의 스크립트들은 `from fasta import ...` 로 같은 `src` 폴더에서 불러온다. 다른 lab 폴더에서 쓰려면 `sys.path` 에 `lab07/src` 를 넣어야 한다.
- 알려진 한계: `read_fasta` 는 첫 줄이 `>` 가 아니면 에러가 나고, 이름이 겹치면 덮어쓴다. `reverse_complement` 는 `N`·소문자에서 `KeyError` 가 난다. `read_fasta` 는 서열을 대문자로 바꿔 돌려준다.

## 코드를 쓸 때
- FASTA 파일은 lab07/src/fasta.py 의 read_fasta 로 읽는다.
- 새 라이브러리(Biopython 등)를 쓰기 전에 먼저 물어본다.
- 주석은 한국어로 쓴다.

## 하지 말 것
- rm 으로 파일을 지우지 않는다.
- pip install 로 무언가를 설치하지 않는다.
- git 명령어를 실행하지 않는다. (README 의 `git add/commit/push` 안내는 학생이 직접 하는 절차이다.)
- 시퀀싱 데이터(`*.fastq`, `*.fq.gz`, `*.sra`)와 조립·주석 결과 폴더(`shovill_out/`, `prokka_out/` 등)는 `.gitignore` 로 제외된다. 용량이 크므로 저장소에 넣으려 하지 말고, 필요하면 wget 등으로 다시 내려받는다.
