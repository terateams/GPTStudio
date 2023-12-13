import streamlit as st
import os
import sys
from dotenv import load_dotenv
from libs.knowledge import search_knowledge, knowledge_dictionary
from libs.msal import msal_auth
from llama_index import VectorStoreIndex, SimpleDirectoryReader

sys.path.append(os.path.abspath('..'))
load_dotenv()


# Authenticate the user via the msal_auth() function
with st.sidebar:
    value = msal_auth()
    if value is None:
        st.stop()

st.markdown("## 📚 知识库搜索")
st.markdown("知识库检索，输入主题，检索相关知识。")


if "knowledge_messages" not in st.session_state.keys():
    st.session_state.knowledge_messages = [{"role": "assistant", "content": "欢迎使用知识库检索， 请输入主题"}]

collection = st.sidebar.selectbox("选择知识库", knowledge_dictionary.keys())
collection_value = knowledge_dictionary[collection]

for knowledge_messages in st.session_state.knowledge_messages:
    with st.chat_message(knowledge_messages["role"]):
        st.write(knowledge_messages["content"])


def clear_chat_history():
    st.session_state.knowledge_messages = [{"role": "assistant", "content": "欢迎使用知识库检索，请输入主题"}]


st.sidebar.button('清除历史', on_click=clear_chat_history)


if prompt := st.chat_input("输入检索主题"):
    st.session_state.knowledge_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.knowledge_messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = search_knowledge(collection_value, prompt)
            if response is None:
                response = "没有找到相关知识"
            st.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.knowledge_messages.append(message)
