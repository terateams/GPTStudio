from dotenv import load_dotenv

load_dotenv()
import streamlit as st
from common.models import get_db_session, get_user_by_usercode
import os

st.set_page_config(
    page_title="GPTStudio",
    page_icon=":material/two_pager:",
    initial_sidebar_state="expanded",
    layout="wide",
)

st.logo("assets/gptstudio-logo.png", icon_image="assets/gptstudio-icon.png", size="large")

pages = {}

gpt_pages = [
    st.Page(
        "gptstudio/PDFReading.py",
        title="PDF 处理",
        icon=":material/two_pager:",
        default=True,
    ),
    st.Page(
        "gptstudio/ImageTools.py",
        title="图像工具",
        icon=":material/psychology:",
    ),
    st.Page(
        "gptstudio/TextToSpeech.py",
        title="文本转语音",
        icon=":material/two_pager:",
    ),
    st.Page(
        "gptstudio/SpeechToText.py",
        title="语音转文本",
        icon=":material/two_pager:",
    ),
    st.Page(
        "gptstudio/RagSubmit.py",
        title="RAG 数据提交",
        icon=":material/two_pager:",
    ),
    st.Page(
        "gptstudio/RagSearch.py",
        title="RAG 数据检索",
        icon=":material/two_pager:",
    )
]

pgm = st.navigation(gpt_pages)
pgm.run()
