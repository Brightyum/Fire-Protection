from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

# from split import Split
from RAG.split import Split


class VectorStore:
    def __init__(self):
        load_dotenv()
        self.splitter = Split()
        self.faiss_path = "./vectorstore"

    def get_embedding_model(self):
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        return embedding_model

    def get_documents(self) -> list[Document]:
        # Document 객체로 초기화
        documents = self.splitter.get_splits()

        return documents

    def get_vectorstore(self):
        documents = self.get_documents()
        embedding_model = self.get_embedding_model()
        vectorstore = None

        batch_size = 50
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i : i + batch_size]
            print(f"임베딩 중입니다. 남은 문서 {len(documents) - i}")

            if vectorstore is None:
                vectorstore = FAISS.from_documents(
                    documents=batch_docs, embedding=embedding_model
                )
            else:
                vectorstore.add_documents(batch_docs)

        return vectorstore

    # 파일이 없으면 자동화 해야함
    def save_vectorstore(self):
        vectorstore = self.get_vectorstore()
        vectorstore.save_local(self.faiss_path)
        print("백터 스토어 저장 완료")

    def load_vectorstore(self):
        embedding_model = self.get_embedding_model()

        vectorstore = FAISS.load_local(
            self.faiss_path,
            embedding_model,
            allow_dangerous_deserialization=True,  # 벡터스토어를 로드할때 .pkl 파일의 역질렬화 허용
        )

        return vectorstore


if __name__ == "__main__":
    test = VectorStore()

    test.save_vectorstore()
