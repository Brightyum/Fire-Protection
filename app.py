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


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.chat = ChatSystem()
        self.setup_routes()

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
        question = request.form.get("question", "")
        if not question:
            return "질문을 입력하세요.", 400

        return Response(self.generate_stream(question), content_type="text/plain")

    # 토큰 스트리밍
    def generate_stream(self, question: str):
        stream = True

        for chunk in self.chat.run(question, stream):
            yield chunk

    # 서버 실행
    def run(self):
        self.app.run(debug=True)
