from llama_index.readers.pdf_marker import PDFMarkerReader
import os

os.environ["PDFTEXT_CPU_WORKERS"] = "1"

# PDF 파일 경로 리스트
pdf_file_path_list = [
    # "PDF\재난현장표준작전절차.pdf", # 원본
    "PDF\재난현장표준작전절차_지휘통제절차.pdf", # 지휘통제절차 SOP 100번대
    # "PDF\재난현장표준작전절차_화재유형별 표준작전절차.pdf", # 화재유형 SOP 200번대
    # "PDF\재난현장표준작전절차_사고유형별 표준작전절차.pdf", # 사고유형 SOP 300번대
    # "PDF\재난현장표준작전절차_구급 단계별 표준작전절차.pdf",  # 구급유형 SOP 400번대
    # "PDF\재난현장표준작전절차_상황 단계별 표준작전절차.pdf", # 상황유형 SOP 500번대
    # "PDF\재난현장표준작전절차_현장 안전관리 표준지침.pdf" # 현장 안전관리 표준지침 SSG 1~8
]
# MarkDown 파일 경로 리스트
md_file_path_list = [
    # "MD\재난현장표준작전절차.pdf", # 원본
    "backUp\재난현장표준작전절차_지휘통제절차.md", # 지휘통제절차 SOP 100번대
    # "MD\재난현장표준작전절차_화재유형별 표준작전절차.md", # 화재유형 SOP 200번대
    # "MD\재난현장표준작전절차_사고유형별 표준작전절차.md", # 사고유형 SOP 300번대
    # "MD\재난현장표준작전절차_구급 단계별 표준작전절차.md",  # 구급유형 SOP 400번대
    # "MD\재난현장표준작전절차_상황 단계별 표준작전절차.md", # 상황유형 SOP  500번대
    # "MD\재난현장표준작전절차_현장 안전관리 표준지침.md" # 현장 안전관리 표준지침 SSG 1~8
]

def pdf_to_md():
    reader = PDFMarkerReader()
    md_file_idx = 0

    for path in pdf_file_path_list:
        documents = reader.load_data(path)
        print(type(documents))

        with open(md_file_path_list[md_file_idx], "w", encoding="utf-8") as file:
            for doc in documents:
                file.write(doc.text)


        print(f"변환 완료: {md_file_path_list[md_file_idx]}")
        md_file_idx += 1


if __name__ == "__main__":
    pdf_to_md()
