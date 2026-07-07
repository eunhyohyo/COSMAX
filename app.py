import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스테빌리티 트래커", layout="wide")

APP_DIR = Path(__file__).parent
HTML_PATH = APP_DIR / "index.html"

IMAGE_FILES = {
    "판교.jpg": "image/jpeg",
    "코스맥스.png": "image/png",
}


def to_data_uri(filename: str, mime: str) -> str:
    """이미지 파일을 base64 data URI로 변환한다.

    index.html은 <img src="판교.jpg">, <img src="코스맥스.png"> 처럼
    상대경로로 이미지를 참조하는데, Streamlit에서 components.html(srcdoc)로
    HTML을 iframe에 넣으면 상대경로 파일을 찾지 못한다.
    그래서 이미지를 base64로 인코딩해 HTML 문자열 안에 직접 삽입한다.
    """
    path = APP_DIR / filename
    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


@st.cache_data
def load_html() -> str:
    html = HTML_PATH.read_text(encoding="utf-8")
    for filename, mime in IMAGE_FILES.items():
        data_uri = to_data_uri(filename, mime)
        html = html.replace(f'src="{filename}"', f'src="{data_uri}"')
    return html


html_content = load_html()

# 업로드 -> 처리중 -> 결과(표+차트) 화면까지 모두 한 페이지 안에서
# JS로 전환되는 구조라서, 넉넉한 높이 + 내부 스크롤을 켜서 렌더링한다.
components.html(html_content, height=1400, scrolling=True)
