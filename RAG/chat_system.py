from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationSummaryMemory
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from RAG.vectorstore import VectorStore


class ChatSystem:
    def __init__(self):
        load_dotenv()
        self.vectorstore = VectorStore().load_vectorstore()
        self.data_first_idx = 0
        
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
                You are an AI coordination officer specialized in analyzing multi-party conversations occurring during disaster response operations.  
                Your primary task is to generate clear, structured responses based on official SOPs (Standard Operating Procedures).  
                Your responsibilities include:
                1. Synthesizing the current situation and establishing a priority for response actions.
                2. Identifying any missing SOP procedures or actions in the dialogue and suggesting supplements.
                3. Detecting and correcting any inconsistencies in the chain of command or improper information flow.

                # Input
                - Context: A set of SOP documents retrieved based on the current situation. Use only this content as your reference.
                - Dialogue: A multi-party log of utterances, including speaker names and timestamps.

                # Instructions
                - Provide a response that presents a clear, step-by-step response strategy.
                - Explicitly mention the relevant SOP numbers and titles, along with explanations of their relevance.
                - If any SOP procedures are omitted or incorrectly followed, suggest what should be added or revised and why.
                - If you detect any breakdown in communication flow or chain-of-command issues, clearly point them out and provide corrections.

                # Output Style
                - Write in concise, logical Korean paragraphs.
                - When appropriate, organize your response using bullet points or numbered lists in the following format:

                Example:
                1. **Initial Response**: According to SOP 212, [details...]
                2. **On-Site Control**: SOP 308 is missing. Commander’s reconfirmation is needed.
                3. **Support Request**: Fire truck dispatch is appropriate, but emergency personnel are not yet requested.

                - At the end of your response, cite the SOP sources used like this:
                - (e.g., *SOP 212: Response Procedures for General Building Fires*)

                # Constraints
                - Do not include any information beyond the provided context. Avoid assumptions or general knowledge.
                - Your entire response **must be written in Korean**.
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

    def get_summary(self):
        llm = self.get_llm()
        
        summary = ConversationSummaryMemory(
            llm=llm,
            return_messages=True,
            output_key=""
        )
        return summary

    def get_json_to_text(self, datas):
        summary = self.get_summary()
        data_last_idx = len(datas) - 1

        for idx, data in enumerate(datas):
            name = data["이름"]
            content = data["내용"]
            if idx == self.data_first_idx:
                time = data["시간"]

                summary.save_context(
                    inputs={f"{name}":f"상황 대화 시작시간({time}): 대화 내용{content}"},
                    outputs={"":""}
                )
                continue
            elif idx == data_last_idx:
                time = data["시간"]

                summary.save_context(
                    inputs={f"{name}":f"상황 대화 끝시간({time}): 대화 내용{content}"},
                    outputs={"":""}
                )
                continue
            
            summary.save_context(
                inputs={f"{name}":f"{content}"},
                outputs={"":""}
            )
            
        result = summary.buffer

        return result

    def run(self, all_data, stream=False):
        # print(f"모든 내용: {all_data}")

        dialogue_text = self.get_json_to_text(all_data)
        print(f"요약내용: {dialogue_text}")

        docs = self.vectorstore.similarity_search(dialogue_text, k=4)

        contents = []
        for doc in docs:
            contents.append(doc.page_content)

        context = "\n\n".join(contents)

        chain = self.get_chain(stream)

        inputs = {"context": context, "data": dialogue_text}

        if stream:
            return chain.stream(inputs)
        else:
            return chain.invoke(inputs)
        

