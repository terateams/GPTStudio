import streamlit as st
import sys
import os
from dotenv import load_dotenv
from apps.chatbot import get_chatbot_page
from libs.msal import msal_auth

sys.path.append(os.path.abspath('..'))
load_dotenv()

with st.sidebar:
    value = msal_auth()
    if value is None:
        st.stop()


st.markdown("## 💡Python 编程导师")

get_chatbot_page("codeboy", "codeboy", mr_ranedeer=True)
