from langchain_core.documents import Document
import os

class Load:
    def __init__(self):
        self.txt_file_path_list = [
            "TXT\재난현장표준작전절차.txt", # 원본
            "TXT\재난현장표준작전절차_지휘통제절차.txt", # 지휘통제절차 SOP 100번대
            "TXT\재난현장표준작전절차_화재유형별 표준작전절차.txt", # 화재유형 SOP 200번대
            "TXT\재난현장표준작전절차_사고유형별 표준작전절차.txt", # 사고유형 SOP 300번대
            "TXT\재난현장표준작전절차_구급 단계별 표준작전절차.txt", # 구급유형 SOP 400번대
            "TXT\재난현장표준작전절차_상황 단계별 표준작전절차.txt", # 상황유형 SOP  500번대
            "TXT\재난현장표준작전절차_현장 안전관리 표준지침.txt" # 현장 안전관리 표준지침 SSG 1~8
        ]
        self.document_list = []

    def get_document_list(self) -> list[Document]:

        for file_path in self.txt_file_path_list:
            
            # 파일 읽기
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

                metadata = {
                    "source": os.path.basename(file_path),
                    "category": self.get_category_from_filename(file_path)
                }

                document = Document(
                    page_content=content,
                    metadata=metadata
                )
                
                self.document_list.append(document)
        
        return self.document_list

    def get_category_from_filename(self, file_path: str) -> str:

        if "지휘통제절차" in file_path:
            return "SOP-100"
        elif "화재유형" in file_path:
            return "SOP-200"
        elif "사고유형" in file_path:
            return "SOP-300"
        elif "구급" in file_path:
            return "SOP-400"
        elif "상황" in file_path:
            return "SOP-500"
        elif "안전관리" in file_path:
            return "SSG"
        else:
            return "General"
        

if __name__ == "__main__":
    test = Load()

    result = test.get_document_list()

    for doc in result:
        print(f"📄 Source: {doc.metadata['source']} / Category: {doc.metadata['category']}")
        print(doc.page_content[:100], "...")
        print(f"\n{'-' * 100}\n")
        
