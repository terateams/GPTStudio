import streamlit as st
import os
import sys
from dotenv import load_dotenv
from libs.knowledge import search_knowledge, knowledge_dictionary
from libs.llama_utils import get_llama_store_index, create_document_index
from libs.msal import msal_auth
from llama_index import VectorStoreIndex, SimpleDirectoryReader

sys.path.append(os.path.abspath('..'))
load_dotenv()

# Authenticate the user via the msal_auth() function
with st.sidebar:
    value = msal_auth()
    if value is None:
        st.stop()

st.markdown("## 🌐 Radius RFC 搜索")
st.markdown("RADIUS RFC 文档检索，输入主题，检索相关内容。")

index = get_llama_store_index("radiusrfc.chroma.db", "radiusrfc")
query = index.as_query_engine()

if "radiusefc_messages" not in st.session_state.keys():
    st.session_state.radiusefc_messages = [
        {"role": "assistant", "content": "欢迎使用 RADIUS RFC 知识库检索， 请输入主题"}]

for radiusefc_messages in st.session_state.radiusefc_messages:
    with st.chat_message(radiusefc_messages["role"]):
        st.markdown(radiusefc_messages["content"])


def clear_chat_history():
    st.session_state.radiusefc_messages = [
        {"role": "assistant", "content": "欢迎使用 RADIUS RFC 知识库检索，请输入主题"}]


with st.sidebar:
    if st.button('构建知识库'):
        with st.spinner("构建中..."):
            create_document_index(
                "libs/assets/radius_rfc",
                "radiusrfc.chroma.db",
                "radiusrfc"
            )
    st.button('清除历史', on_click=clear_chat_history)

if prompt := st.chat_input("输入检索主题"):
    st.session_state.radiusefc_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.radiusefc_messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query.query(prompt)
            st.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.radiusefc_messages.append(message)
