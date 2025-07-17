from PyPDF2 import PdfReader

"""
PDF 파일들을 txt로 전환하는 모듈

"""

# PDF 파일 경로 리스트
pdf_file_path_list = [
    "PDF\재난현장표준작전절차.pdf", # 원본
    "PDF\재난현장표준작전절차_지휘통제절차.pdf", # 지휘통제절차 SOP 100번대
    "PDF\재난현장표준작전절차_화재유형별 표준작전절차.pdf", # 화재유형 SOP 200번대
    "PDF\재난현장표준작전절차_사고유형별 표준작전절차.pdf", # 사고유형 SOP 300번대
    "PDF\재난현장표준작전절차_구급 단계별 표준작전절차.pdf", # 구급유형 SOP 400번대
    "PDF\재난현장표준작전절차_상황 단계별 표준작전절차.pdf", # 상황유형 SOP  500번대
    "PDF\재난현장표준작전절차_현장 안전관리 표준지침.pdf" # 현장 안전관리 표준지침 SSG 1~8
]
# txt 생성 파일 경로 리스트
txt_file_path_list = [
    "TXT\재난현장표준작전절차.txt", # 원본
    "TXT\재난현장표준작전절차_지휘통제절차.txt", # 지휘통제절차 SOP 100번대
    "TXT\재난현장표준작전절차_화재유형별 표준작전절차.txt", # 화재유형 SOP 200번대
    "TXT\재난현장표준작전절차_사고유형별 표준작전절차.txt", # 사고유형 SOP 300번대
    "TXT\재난현장표준작전절차_구급 단계별 표준작전절차.txt", # 구급유형 SOP 400번대
    "TXT\재난현장표준작전절차_상황 단계별 표준작전절차.txt", # 상황유형 SOP  500번대
    "TXT\재난현장표준작전절차_현장 안전관리 표준지침.txt" # 현장 안전관리 표준지침 SSG 1~8
]

txt_file_idx = 0

for file_path in pdf_file_path_list:
    # PdfReader 객체 생성
    reader = PdfReader(file_path)

    pages = reader.pages
    text_list = []

    for page in pages:
        sub = page.extract_text()
        text_list.append(sub)
    
    with open(txt_file_path_list[txt_file_idx], "w", encoding="utf-8") as file:
        for text in text_list:
            file.write(text + "\n")

    txt_file_idx += 1


