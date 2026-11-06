# check_cds.py
# data 폴더의 rbcL_*.gb 파일을 Biopython 으로 읽어서,
# CDS 를 직접 번역(table=11, 엽록체 유전암호)한 결과가
# GenBank 에 적힌 /translation 과 같은지 확인한다.
#
# 실행 방법 (lab10 폴더 안에서):
#     python3 src/check_cds.py
#
# 출력 (탭 구분):
#     파일이름  VERSION  ORGANISM  CDS위치  일치여부

import glob
import os

from Bio import SeqIO
from Bio.SeqFeature import BeforePosition, AfterPosition


def is_partial(feature):
    """CDS 위치에 '<' 나 '>' 가 붙어 있으면(부분 서열이면) True."""
    start = feature.location.start
    end = feature.location.end
    return isinstance(start, BeforePosition) or isinstance(end, AfterPosition)


def genbank_location(feature):
    """Biopython 위치(0부터 셈)를 GenBank 표기(1부터 셈, 예: <1..>1408)로 바꾼다."""
    start = feature.location.start
    end = feature.location.end
    text = ""
    if isinstance(start, BeforePosition):
        text = text + "<"
    text = text + str(int(start) + 1) + ".."
    if isinstance(end, AfterPosition):
        text = text + ">"
    text = text + str(int(end))
    # 역방향 가닥이면 complement( ) 로 감싼다
    if feature.location.strand == -1:
        text = "complement(" + text + ")"
    return text


def translate_cds(feature, record):
    """CDS 를 table=11 로 번역해서 아미노산 문자열로 돌려준다."""
    # CDS 부분의 염기서열을 잘라낸다
    cds_seq = feature.extract(record.seq)

    # /codon_start 가 2나 3이면 그만큼 앞을 건너뛰고 번역을 시작해야 한다
    codon_start = int(feature.qualifiers.get("codon_start", ["1"])[0])
    cds_seq = cds_seq[codon_start - 1:]

    if is_partial(feature):
        # 부분 CDS: 시작/종결 코돈이 없을 수 있으므로 그냥 번역한다.
        # 길이가 3의 배수가 아니면 뒤에 남는 염기는 버린다.
        cds_seq = cds_seq[:len(cds_seq) // 3 * 3]
        protein = str(cds_seq.translate(table=11))
        # 끝에 종결 코돈(*)이 있으면 /translation 에는 없으므로 지운다
        if protein.endswith("*"):
            protein = protein[:-1]
    else:
        # 완전한 CDS: cds=True 로 번역하면
        # 첫 코돈을 M 으로 바꾸고 종결 코돈(*)은 빼 준다
        protein = str(cds_seq.translate(table=11, cds=True))

    return protein


# data 폴더에서 rbcL_*.gb 파일을 이름 순서대로 모두 찾는다
gb_files = sorted(glob.glob("data/rbcL_*.gb"))

# 머리줄 출력
print("file\tversion\torganism\tcds_location\ttranslation_match")

for path in gb_files:
    file_name = os.path.basename(path)

    # 파일 하나에 레코드가 여러 개일 수도 있으므로 반복문으로 읽는다
    for record in SeqIO.parse(path, "genbank"):
        version = record.id                       # 예: KU739560.1
        organism = record.annotations.get("organism", "")

        # 레코드 안의 CDS feature 를 하나씩 확인한다
        for feature in record.features:
            if feature.type != "CDS":
                continue

            location = genbank_location(feature)

            # GenBank 에 적힌 /translation 값 (없으면 빈 문자열)
            given = feature.qualifiers.get("translation", [""])[0]

            if given == "":
                result = "NO_TRANSLATION"
            else:
                try:
                    mine = translate_cds(feature, record)
                    if mine == given:
                        result = "MATCH"
                    else:
                        result = "MISMATCH"
                except Exception as error:
                    # 번역 중 에러(예: 시작 코돈이 아님)가 나면 내용을 보여 준다
                    result = "ERROR: " + str(error)

            print(file_name + "\t" + version + "\t" + organism + "\t"
                  + location + "\t" + result)
