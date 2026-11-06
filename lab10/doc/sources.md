# 데이터 출처

- 받은 날짜: 2026-11-__
- 받은 곳: NCBI Nucleotide (E-utilities esearch + efetch)
- 받은 방법: src/get_rbcL.sh (Claude Code가 작성, wget 사용)
- 검색어: rbcL[Gene] AND 학명[Organism] AND 1300:1500[SLEN], 첫 번째 결과만 받음

## 확인에 쓴 명령어 (모두 직접 실행)

| 기호 | 명령어 | 확인한 것 |
|---|---|---|
| A | grep "^VERSION" data/rbcL_*.gb | 접근번호와 버전 |
| B | grep "  ORGANISM" data/rbcL_*.gb | 요청한 종이 맞는지 |
| C | for F in data/rbcL_*.fa; do python3 src/fasta.py "$F"; done | 서열 길이 |
| D | grep -c ">" data/rbcL_*.fa | 파일마다 서열이 1개인지 |
| E | python3 src/check_cds.py > doc/cds_check.tsv | CDS 위치와 번역 일치 |
| F | grep "^ACCESSION" data/rbcL_*.gb, grep "^DEFINITION" data/rbcL_*.gb | 유전체 일부를 잘라 받은 레코드(REGION)인지 확인 |
| G | python3 src/compare.py data/rbcL_all.fasta | fasta.py와 Biopython 길이 비교 |

## 출처 표

| 파일 | VERSION | ORGANISM | 길이 | CDS 위치 | 번역 일치 | 확인 방법 | 문제 |
|---|---|---|---|---|---|---|---|
| rbcL_arabidopsis | KU739560.1 | Arabidopsis thaliana | 1408 | <1..>1408 | MATCH | A, B, C, D, E, F, G | 앞뒤가 잘린 부분 CDS. 번역은 일치 |
| rbcL_ginseng | MT416077.1 | Panax ginseng | 1458 | 1..1458 | MATCH | A, B, C, D, E, F, G | 8종 중 유일하게 ACCESSION에 "REGION: 57343..58800"이 붙어 있음. DEFINITION이 "chloroplast, complete genome"으로, 엽록체 유전체 전체 레코드에서 rbcL 구간만 잘라 받은 것. 에이전트가 지시하지 않은 방법을 썼음 |
| rbcL_rice | LT576846.1 | Oryza sativa Japonica Group | 1389 | 1..>1389 | MATCH | A, B, C, D, E, F, G | 뒤가 잘린 부분 CDS. ORGANISM이 품종군(Japonica Group)까지 표시됨 |
| rbcL_maize | Z11973.1 | Zea mays | 1431 | 1..1431 | MATCH | A, B, C, D, E, F, G | 없음. DEFINITION이 "Z.mays chloroplast rbcL gene"으로 rbcL만 담은 레코드이고 ACCESSION에 REGION 없음 |
| rbcL_ginkgo | KF221173.1 | Ginkgo biloba | 1317 | <1..>1317 | MATCH | A, B, C, D, E, F, G | 앞뒤가 잘린 부분 CDS. 번역은 일치 |
| rbcL_pine | JQ512595.1 | Pinus thunbergii | 1428 | 1..1428 | MATCH | A, B, C, D, E, F, G | 없음 |
| rbcL_fern | MW620303.1 | Adiantum capillus-veneris | 1308 | <1..>1308 | MATCH | A, B, C, D, E, F, G | 앞뒤가 잘린 부분 CDS. 번역은 일치 |
| rbcL_liverwort | LC536762.1 | Marchantia polymorpha subsp. ruderalis | 1399 | <1..1399 | MATCH | A, B, C, D, E, F, G | 앞이 잘린 부분 CDS. 요청한 종의 아종(subsp. ruderalis)이 받아짐 |

## 13번 · fasta.py와 Biopython 비교

명령어: python3 src/compare.py data/rbcL_all.fasta
결과: 여덟 줄 중 True ___개

## 16번 · CDS 번역 확인

- 스크립트: src/check_cds.py (Claude Code가 작성, 실행과 확인은 직접 함)
- 일치하지 않은 종 수 (cut -f5 doc/cds_check.tsv | sort | uniq -c): 0개, 8종 모두 MATCH
- 15번에서 손으로 확인한 애기장대 결과(mine == ncbi → True)와 스크립트 결과(MATCH)가 같다
- <, > 가 붙은 부분 CDS가 5종(애기장대, 벼, 은행나무, 공작고사리, 우산이끼)이지만 모두 1번 염기에서
  codon_start=1로 시작해 코돈 틀이 맞으므로 NCBI 번역과 일치했다
- 참고: 지시에는 "같은지"를 출력하라고 했는데 스크립트는 True/False 대신 MATCH로 출력했다.
  그래서 grep -c "False"로는 셀 수 없어서 cut과 uniq -c로 셌다

## 점검

1. ORGANISM이 요청한 종과 정확히 같은가: 6종은 같음. 우산이끼는 아종(subsp. ruderalis), 벼는 품종군(Japonica Group)으로 표시됨
2. 길이가 모두 1,300~1,500 사이인가: 예 (1308 ~ 1458)
3. 파일마다 서열이 하나씩인가: ___
4. 합친 파일 data/rbcL_all.fasta의 서열 수: ___
5. 유전체 일부를 잘라 받은 레코드: 인삼 1개 (grep "^ACCESSION"으로 REGION 확인)

## 문제가 있던 파일과 다시 받을 때의 지시

- rbcL_ginseng: 길이 제한 검색 결과가 없어서 에이전트가 엽록체 유전체에서 구간을 잘라 받은 것으로 보임.
  다시 받는다면: "검색 결과가 0개이면 다른 방법으로 바꾸지 말고 먼저 알려 줘. seq_start, seq_stop, rettype=ft로 구간을 잘라 받는 건 허락할 때만 해."
- rbcL_liverwort: 아종이 받아짐. 정확히 Marchantia polymorpha만 원한다면 ORGANISM을 확인하고
  아종이면 다음 검색 결과를 쓰라고 지시한다.