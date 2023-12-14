import streamlit as st
import sys
import os
from dotenv import load_dotenv
from apps.chatbot import get_chatbot_page
from apps.ragsbot import get_ragsbot_page
from libs.llama_utils import get_llama_memary_index
from libs.msal import msal_auth

sys.path.append(os.path.abspath('..'))
load_dotenv()

with st.sidebar:
    value = msal_auth()
    if value is None:
        st.stop()

st.markdown("## 🌟 Rags Bot")
st.markdown("基于 LlamaIndex 的人工智能学习导师，可以解读各种文件")

get_ragsbot_page("ragsbot")

