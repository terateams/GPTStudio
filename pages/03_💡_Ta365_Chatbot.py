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


st.markdown("## 💡 Ta365")
st.markdown("博学多才的人工智能学习导师，可以帮助学生解决各种学习上的问题")

get_chatbot_page("ta365", "ta365", mr_ranedeer=True)
