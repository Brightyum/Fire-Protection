# txt 파일 경로 리스트
txt_file_path_list = [
    "TXT\재난현장표준작전절차.txt", # 원본
    "TXT\재난현장표준작전절차_지휘통제절차.txt", # 지휘통제절차 SOP 100번대
    "TXT\재난현장표준작전절차_화재유형별 표준작전절차.txt", # 화재유형 SOP 200번대
    "TXT\재난현장표준작전절차_사고유형별 표준작전절차.txt", # 사고유형 SOP 300번대
    "TXT\재난현장표준작전절차_구급 단계별 표준작전절차.txt", # 구급유형 SOP 400번대
    "TXT\재난현장표준작전절차_상황 단계별 표준작전절차.txt", # 상황유형 SOP  500번대
    "TXT\재난현장표준작전절차_현장 안전관리 표준지침.txt" # 현장 안전관리 표준지침 SSG 1~8
]

# 특정 반복 문장
target = "Standard  Operating  Procedures  in Disaster  Site"

for file_path in txt_file_path_list:
    
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()

        # 빈 줄 제거
        if not stripped:
            continue
        
        # 한 글자 줄 제거
        if len(stripped) == 1:
            continue
        
        # 특정 반복 문장 제거
        if stripped == target:
            continue
        
        cleaned_lines.append(line)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)
    
    print(f"전처리 완료: {file_path}")
