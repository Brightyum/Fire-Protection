from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document
# from RAG.load import Load
from load import Load


class Split:
    def __init__(self):
        self.load = Load()
        self.splits = []
        self.chunk_size = 500
        self.chunk_overlap = 100

    def get_header_split(self):
        header_to_split_on = [
            ("#", "Header"),
            ("##", "SubTitle"),
            ("###", "Sub-SubTitle"),
        ]
        return header_to_split_on

    def get_md_splitter(self):
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.get_header_split(), strip_headers=False
        )
        return md_splitter

    def get_md_splits(self) -> list[Document]:
        md_splitter = self.get_md_splitter()
        md_splits = []

        for md in self.load.load_markdown():
            splits = md_splitter.split_text(md)

            md_splits.extend(splits)

        return md_splits

    def get_rc_splitter(self):
        rc_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n\n", "\n\n", "\n", ".", " ", ""],
        )
        return rc_splitter

    def get_splits(self) -> list[Document]:
        rc_splitter = self.get_rc_splitter()
        md_splits = self.get_md_splits()

        for doc in md_splits:
            chunks = rc_splitter.split_text(doc.page_content)

            for chunk in chunks:
                self.splits.append(Document(page_content=chunk, metadata=doc.metadata))

        return self.splits


if __name__ == "__main__":
    split = Split()
    result1 = split.get_md_splits()
    result2 = split.get_splits()
    # print(len(result))

    # for i in result1[3:7]:
    #     print(i)

    for i in result2[5:10]:
        print(i)