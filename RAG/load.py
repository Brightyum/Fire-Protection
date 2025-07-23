from langchain_core.documents import Document
import os


class Load:
    def __init__(self):
        self.md_file_path_list = [
            # "PDF\재난현장표준작전절차.pdf", # 원본
            ".\MD\재난현장표준작전절차_지휘통제절차.md", # 지휘통제절차 SOP 100번대
            ".\MD\재난현장표준작전절차_화재유형별 표준작전절차.md", # 화재유형 SOP 200번대
            ".\MD\재난현장표준작전절차_사고유형별 표준작전절차.md", # 사고유형 SOP 300번대
            ".\MD\재난현장표준작전절차_구급 단계별 표준작전절차.md",  # 구급유형 SOP 400번대
            ".\MD\재난현장표준작전절차_상황 단계별 표준작전절차.md", # 상황유형 SOP  500번대
            # "MD\재난현장표준작전절차_현장 안전관리 표준지침.md" # 현장 안전관리 표준지침 SSG 1~8
        ]
        self.md_list = []

    def load_markdown(self) -> list:
        for path in self.md_file_path_list:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            self.md_list.append(content)

        return self.md_list

if __name__ == "__main__":
    loader = Load()

    result = loader.load_markdown()

    print(len(result))
