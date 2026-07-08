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


def load_html() -> str:
    """매 실행(rerun)마다 index.html을 다시 읽는다.

    st.cache_data로 캐싱하면 index.html만 수정했을 때 반영되지 않고 예전
    내용이 계속 떠서(로컬 재시작 전까지, 또는 배포 환경의 캐시 정책에 따라)
    혼란을 주므로, 파일이 작아 매번 새로 읽어도 비용이 무시할 만한 점을
    감안해 캐싱하지 않는다.
    """
    html = HTML_PATH.read_text(encoding="utf-8")
    for filename, mime in IMAGE_FILES.items():
        data_uri = to_data_uri(filename, mime)
        html = html.replace(f'src="{filename}"', f'src="{data_uri}"')
    return html


html_content = load_html()

# 업로드 -> 처리중 -> 결과(표+차트) 화면까지 모두 한 페이지 안에서
# JS로 전환되는 구조라서, 넉넉한 높이 + 내부 스크롤을 켜서 렌더링한다.
components.html(html_content, height=1400, scrolling=True)
