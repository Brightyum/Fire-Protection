from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from RAG.vectorstore import VectorStore
from RAG.memory_manager import MemoryManager


class ChatSystem:
    def __init__(self):
        load_dotenv()
        self.vectorstore = VectorStore().load_vectorstore()
        self.memory = MemoryManager()

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
                Analyzes conversations between users and points out missing SOP procedures or corrections.
                You must answer in Korean.

                # Instruction
                Generate a clear, operationally structured answer by logically integrating the retrieved content. 
                Use complete paragraphs, but apply concise expression. 
                Specify the SOP number and name in a footnote.
                If any SOP procedures are missing, supplement them with documentation and provide explanations.

                # Constraint
                - Only use information from the given context.
                - Do not invent facts or draw from general world knowledge.
                - When possible, include the SOP number and name in the answer footer.
  
              """,
            ),
            ("human", "#Context: {context}\n#Dialogue: {data}"),
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

    def get_json_to_text(self, datas):
        lines = []
        for data in datas:
            name = data["이름"]
            content = data["내용"]
            time = data["시간"]
            line = f"{name}: {content}({time})"
            lines.append(line)

        result = "\n".join(lines)
        return result

    def run(self, all_data, stream=False):
        dialogue_text = self.get_json_to_text(all_data)

        docs = self.vectorstore.similarity_search(dialogue_text, k=4)

        contents = []
        for doc in docs:
            contents.append(doc.page_content)

        context = "\n\n".join(contents)

        data = self.memory.get_recent_data()

        chain = self.get_chain(stream)

        inputs = {"context": context, "data": dialogue_text}

        if stream:
            return chain.stream(inputs)
        else:
            return chain.invoke(inputs)
