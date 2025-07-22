from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAG.load import Load

class Split:
    def __init__(self):
        self.load = Load()
    
    def get_splitter(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50,
            
        )