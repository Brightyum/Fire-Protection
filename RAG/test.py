from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

# 1. 벡터스토어 로딩
vectorstore = FAISS.load_local("./faiss_index", OpenAIEmbeddings(),allow_dangerous_deserialization=True)

# 2. 질의 입력 및 유사 문서 검색
query = "SOP 212에서 일반 건축물 화재 대응 시 주의사항은?"
docs_and_scores = vectorstore.similarity_search_with_score(query, k=4)

# 3. 점수만 추출
scores = [score for _, score in docs_and_scores]

# 4. 시각화 (꺾은선 그래프 + 임계값 표시)
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(scores) + 1), scores, marker='o', label='Similarity Scores')

# 예: 임계값을 0.75로 설정
threshold = 0.75
plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold})')

print(f"FAISS index 벡터 수: {vectorstore.index.ntotal}")

for i, (doc, score) in enumerate(docs_and_scores, 1):
    print(f"[{i}] 유사도 점수: {score:.4f}")
    print(f"내용: {doc.page_content[:100]}...\n")  # 앞 100자만 확인


plt.xlabel("Retrieved Document Index")
plt.ylabel("Similarity Score")
plt.title("유사도 점수 및 임계값 시각화")
plt.legend()
plt.grid(True)
plt.show()


