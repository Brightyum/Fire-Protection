from flask import (
    Flask,
    render_template,
    app,
    render_template,
    request,
    Response,
    stream_with_context,
)
from RAG.chat_system import ChatSystem
from RAG.memory_manager import MemoryManager


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.chat = ChatSystem()
        self.memory = MemoryManager()
        self.setup_routes()
        self.max_entries = 20
        self.min_entries = 5

    # 페이지 라우팅 등록
    def setup_routes(self):
        # 메인페이지
        self.app.add_url_rule("/", view_func=self.main_page)
        self.app.add_url_rule("/home", view_func=self.main_page)

        # 스트리밍 응답
        self.app.add_url_rule("/stream", view_func=self.stream_answer, methods=["POST"])

    # 메인 페이지 렌더링
    def main_page(self):
        return render_template("main_page.html")

    # stream 대답 라우팅 핸들러
    def stream_answer(self):
        name = request.form.get("name", "")
        question = request.form.get("question", "")
        if not question and not name:
            return "이름과 질문을 입력하세요.", 400

        return Response(self.generate_stream(question, name), content_type="text/plain")

    # 토큰 스트리밍
    def generate_stream(self, question: str, name: str):
        stream = True

        self.memory.set_data(name, question)
        all_data = self.memory.get_data()

        if len(all_data) < self.min_entries:
            yield "[시스템] 대화가 저장되고 있습니다."
            return

        # if len(all_data) > self.max_entries:
        #     all_data = self.memory.get_recent_data()

        for chunk in self.chat.run(all_data, stream):
            yield chunk

    # 서버 실행
    def run(self):
        self.app.run(debug=True)
