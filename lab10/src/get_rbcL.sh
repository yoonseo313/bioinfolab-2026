#!/bin/bash
# 식물 8종의 rbcL 서열을 NCBI E-utilities 로 내려받는 스크립트
# 실행: cd lab10 && bash src/get_rbcL.sh

# E-utilities 기본 주소
BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# 모든 종의 검색어 뒤에 붙이는 필터: 검증된 유전체(genomic DNA) 레코드만 받는다
#   AND biomol_genomic[PROP] NOT UNVERIFIED  (URL 형식으로 바꿔 쓴 것)
FILTER="+AND+biomol_genomic%5BPROP%5D+NOT+UNVERIFIED"

# "학명|파일이름" 목록
# 인삼(Panax ginseng)은 1300~1500 bp 짜리 rbcL 단독 서열이 없어서
# 아래 반복문이 끝난 뒤 따로 처리한다 (엽록체 유전체에서 rbcL 부위만 잘라 받기)
SPECIES=(
  "Arabidopsis thaliana|rbcL_arabidopsis"
  "Oryza sativa|rbcL_rice"
  "Zea mays|rbcL_maize"
  "Ginkgo biloba|rbcL_ginkgo"
  "Pinus thunbergii|rbcL_pine"
  "Adiantum capillus-veneris|rbcL_fern"
  "Marchantia polymorpha|rbcL_liverwort"
)

for item in "${SPECIES[@]}"; do
  # | 를 기준으로 학명과 파일 이름을 나눈다
  name="${item%%|*}"
  out="${item##*|}"

  # 검색어: rbcL[Gene] AND "학명"[Organism] AND 1300:1500[SLEN]
  #         AND biomol_genomic[PROP] NOT UNVERIFIED
  #   - biomol_genomic[PROP] : 유전체 DNA 레코드만 (mRNA 같은 것은 뺀다)
  #   - NOT UNVERIFIED       : NCBI 가 "검증 안 됨(UNVERIFIED)" 표시를 한 레코드는 뺀다
  # URL 안에서는 띄어쓰기를 +, 따옴표를 %22, 대괄호를 %5B %5D 로 바꿔 써야 한다
  org="${name// /+}"
  term="rbcL%5BGene%5D+AND+%22${org}%22%5BOrganism%5D+AND+1300:1500%5BSLEN%5D${FILTER}"

  # 1) esearch: 첫 번째 결과만 받는다 (retmax=1)
  id=$(wget -qO- "${BASE}/esearch.fcgi?db=nucleotide&term=${term}&retmax=1" \
       | grep -o '<Id>[0-9]*</Id>' | head -1 | sed 's/<[^>]*>//g')
  sleep 1

  # 결과가 없으면 알리고 다음 종으로 넘어간다
  if [ -z "$id" ]; then
    echo "검색 결과 없음: $name"
    continue
  fi
  echo "$name -> ID $id"

  # 2) efetch: FASTA 로 받기
  wget -qO "data/${out}.fa" "${BASE}/efetch.fcgi?db=nucleotide&id=${id}&rettype=fasta&retmode=text"
  sleep 1

  # 3) efetch: GenBank 로 받기
  wget -qO "data/${out}.gb" "${BASE}/efetch.fcgi?db=nucleotide&id=${id}&rettype=gb&retmode=text"
  sleep 1
done

# ----------------------------------------------------------------------
# 인삼: 엽록체 전체 유전체(complete genome)에서 rbcL 부위만 받는다
# ----------------------------------------------------------------------
echo "Panax ginseng: 엽록체 유전체에서 rbcL 부위를 찾는다"

# 1) esearch: 인삼 엽록체 전체 유전체를 찾아 첫 번째 결과만 받는다
#    (다른 종과 같은 검증·유전체 필터 FILTER 를 붙인다)
term="%22Panax+ginseng%22%5BOrganism%5D+AND+chloroplast%5BTitle%5D+AND+complete+genome%5BTitle%5D${FILTER}"
id=$(wget -qO- "${BASE}/esearch.fcgi?db=nucleotide&term=${term}&retmax=1" \
     | grep -o '<Id>[0-9]*</Id>' | head -1 | sed 's/<[^>]*>//g')
sleep 1

if [ -z "$id" ]; then
  echo "검색 결과 없음: Panax ginseng 엽록체 유전체"
else
  # 2) efetch: 특징표(feature table, rettype=ft)를 받아 rbcL 유전자의 위치를 찾는다
  #    특징표에서는 아래처럼 위치 줄 바로 다음 줄에 유전자 이름이 나온다
  #      57343   58800   gene
  #                      gene    rbcL
  #    그래서 "gene rbcL" 줄의 바로 앞 줄(-B1)을 꺼낸다
  loc=$(wget -qO- "${BASE}/efetch.fcgi?db=nucleotide&id=${id}&rettype=ft&retmode=text" \
        | grep -B1 'gene[[:space:]]*rbcL$' | head -1)
  sleep 1

  # 첫째 칸이 시작 위치, 둘째 칸이 끝 위치 (< > 같은 기호는 지운다)
  start=$(echo "$loc" | cut -f1 | tr -dc '0-9')
  stop=$(echo "$loc" | cut -f2 | tr -dc '0-9')

  if [ -z "$start" ] || [ -z "$stop" ]; then
    echo "rbcL 위치를 찾지 못함: ID $id"
  else
    # 시작이 끝보다 크면 반대 가닥(-)에 있는 유전자이다
    # 이때는 숫자 순서를 바꾸고 strand=2 (역상보 서열)로 받는다
    if [ "$start" -lt "$stop" ]; then
      strand=1
    else
      strand=2
      tmp=$start; start=$stop; stop=$tmp
    fi
    echo "Panax ginseng -> ID $id, rbcL ${start}-${stop} (strand ${strand})"

    # 3) efetch: 그 부위만 FASTA 와 GenBank 로 받는다
    region="seq_start=${start}&seq_stop=${stop}&strand=${strand}"
    wget -qO "data/rbcL_ginseng.fa" "${BASE}/efetch.fcgi?db=nucleotide&id=${id}&${region}&rettype=fasta&retmode=text"
    sleep 1
    wget -qO "data/rbcL_ginseng.gb" "${BASE}/efetch.fcgi?db=nucleotide&id=${id}&${region}&rettype=gb&retmode=text"
    sleep 1
  fi
fi

# 받은 파일의 첫 줄을 확인한다
head -1 data/rbcL_*.fa
