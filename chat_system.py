from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

TXT_FILE_PATH = "TXT\SOP_100~109.txt"

class ChatSystem():
    def __init__(self):
        load_dotenv()

    # txt파일에서 텍스트를 읽어 저장
    def get_system_prompt_txt(self) -> str:
        with open(TXT_FILE_PATH, "r", encoding="utf-8") as file:
            txt_read = file.read()
        
        return txt_read
    
    # 거대언어모델 openAI gpt-4o로 생성
    def get_llm(self, stream=False):
        return ChatOpenAI(model="gpt-4o", temperature=0.2, streaming=stream)
    
    # 프롬프트 메시지 생성
    def get_messages(self):
        txt_read = self.get_system_prompt_txt()

        # 프롬프트 메시지
        messages = [
            ("system", 
             f"""
              You are a helpful assistant that answer in Korean, 
              Your role is defined by [다음의 글] and you should be clearly aware of [다음의 글]. [다음의 글]: {txt_read}   
              """
            ),
            ("human", "#Question: {question}")
        ]

        return messages

    # 프롬프트 생성
    def get_prompt(self):
        messages = self.get_messages()
        return ChatPromptTemplate.from_messages(messages)

    # 체인 생성
    def get_chain(self, stream=False):
        prompt = self.get_prompt()
        llm = self.get_llm(stream)
        
        return prompt | llm | StrOutputParser()




