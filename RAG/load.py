from langchain_core.documents import Document
import os


class Load:
    def __init__(self):
        self.txt_file_path_list = [
            "TXT\재난현장표준작전절차.txt",  # 원본
            "TXT\재난현장표준작전절차_지휘통제절차.txt",  # 지휘통제절차 SOP 100번대
            "TXT\재난현장표준작전절차_화재유형별 표준작전절차.txt",  # 화재유형 SOP 200번대
            "TXT\재난현장표준작전절차_사고유형별 표준작전절차.txt",  # 사고유형 SOP 300번대
            "TXT\재난현장표준작전절차_구급 단계별 표준작전절차.txt",  # 구급유형 SOP 400번대
            "TXT\재난현장표준작전절차_상황 단계별 표준작전절차.txt",  # 상황유형 SOP  500번대
            "TXT\재난현장표준작전절차_현장 안전관리 표준지침.txt",  # 현장 안전관리 표준지침 SSG 1~8
        ]
        self.documents = []

    def load_chunks_to_document(self):
        """
        각 txt 파일에서 SOP 단위로 분할된 덩어리 리스트를 반환
        """

        for file_path in self.txt_file_path_list:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            chunks = []
            current_chunk = ""

            for line in lines:
                if line.strip().startswith("SOP"):
                    if current_chunk:
                        # 기존 chunk를 저장하고 새로운 chunk 시작
                        chunks.append(current_chunk.strip())
                        current_chunk = ""

                current_chunk += line  # SOP든 아니든 현재 chunk에 추가

            if current_chunk:  # 마지막 덩어리 추가
                chunks.append(current_chunk.strip())

            for chunk in chunks:
                metadata = {
                    "source": os.path.basename(file_path),
                    "category": self.get_category_from_filename(file_path),
                }

                document = Document(page_content=chunk, metadata=metadata)

                self.documents.append(document)

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

    def get_documents(self):
        return self.documents


if __name__ == "__main__":
    loader = Load()
    # sop_chunks = loader.load_chunks()

    # for i, chunk in enumerate(sop_chunks[10:20]):
    #     print(f"\n SOP 문서 {i+1} ------------------")
    #     print(chunk)
    loader.load_chunks_to_document()
    result = loader.get_documents()

    for doc in result:
        print(
            f" Source: {doc.metadata['source']} / Category: {doc.metadata['category']}"
        )
        print(doc.page_content[:100], "...")
        print(f"\n{'-' * 100}\n")
