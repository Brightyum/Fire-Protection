from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from RAG.vectorstore import VectorStore


class ChatSystem:
    def __init__(self, vectorestore_path="./faiss_index"):
        load_dotenv()
        self.vectorstore = VectorStore().load_vectorstore()

    # 거대언어모델 openAI gpt-4o로 생성
    def get_llm(self, stream=False):
        return ChatOpenAI(model="gpt-4o", temperature=0.2, streaming=stream)

    # 프롬프트 메시지 생성
    def get_messages(self):
        # 프롬프트 메시지
        messages = [
            (
                "system",
                """
              # Role
                You are an AI assistant specialized in disaster response domain, especially command-control (지휘통제) and SOP-based operations. 
                You work within a Retrieval-Augmented Generation (RAG) pipeline to answer mission-critical queries.

                # Instruction
                Generate a clear, operationally structured answer by logically integrating the retrieved content. 
                Use complete paragraphs, but apply concise expression. 
                When the question involves a process, list steps in order. Use SOP-specific terminology where possible.

                # Constraint
                - Only use information from the given context.
                - Do not invent facts or draw from general world knowledge.
                - When possible, include the SOP number and name in the answer footer.
  
              """,
            ),
            ("human", "#Context: {context}\n#Question: {question}"),
        ]

        return messages

    def get_prompt(self):
        messages = self.get_messages()
        return ChatPromptTemplate.from_messages(messages)

    # 체인 생성
    def get_chain(self, stream=False):
        prompt = self.get_prompt()
        llm = self.get_llm(stream)

        return prompt | llm | StrOutputParser()

    def run(self, question: str, stream=False):
        docs = self.vectorstore.similarity_search(question, k=4)

        contents = []
        for doc in docs:
            contents.append(doc.page_content)

        context = "\n\n".join(contents)

        chain = self.get_chain(stream)

        if stream:
            return chain.stream({"question": question, "context": context})
        else:
            return chain.invoke({"question": question, "context": context})
