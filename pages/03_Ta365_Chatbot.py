import streamlit as st
import sys
import os
from dotenv import load_dotenv
from libs.knowledge import knowledge_dictionary, search_knowledge
from libs.prompts import get_ta365_sysmsg
from libs.msal import msal_auth
from libs.llms import openai_streaming
from libs.session import PageSessionState

sys.path.append(os.path.abspath('..'))
load_dotenv()

page_state = PageSessionState("ta365")

with st.sidebar:
    value = msal_auth()
    if value is None:
        st.stop()

st.sidebar.markdown("# 💡Ta365 AI 助手")

welcome_msg = {"role": "assistant", "content": "我是 Ta365 AI 助手，欢迎提问， 左侧栏可以选择知识库"}

# 用于存储对话记录, 第一条为欢迎消息
page_state.initn_attr("messages", [welcome_msg])

# 用于标记上一条用户消息是否已经处理
page_state.initn_attr("last_user_msg_processed", True)

# 用于标记流式输出是否结束
page_state.initn_attr("streaming_end", True)


def end_chat_streaming():
    """当停止按钮被点击时执行，用于修改处理标志"""
    page_state.streaming_end = True
    page_state.last_user_msg_processed = True


def start_chat_streaming():
    """当开始按钮被点击时执行，用于修改处理标志"""
    page_state.streaming_end = False
    page_state.last_user_msg_processed = False


collection = st.sidebar.selectbox("选择知识库", knowledge_dictionary.keys())
collection_value = knowledge_dictionary[collection]

for msg in page_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


def clear_chat_history():
    page_state.messages = [welcome_msg]


st.sidebar.button('清除对话历史', on_click=clear_chat_history)

# 用户输入
if not page_state.last_user_msg_processed:
     st.chat_input("请等待上一条消息处理完毕", disabled=True)
else:
    if prompt := st.chat_input("输入你的问题"):
        page_state.chat_prompt = prompt
        start_chat_streaming()
        page_state.add_chat_msg("messages", {"role": "user", "content": page_state.chat_prompt})
        with st.chat_message("user"):
            st.write(page_state.chat_prompt)
            st.rerun()

stop_action = st.sidebar.empty()
if not page_state.streaming_end:
    stop_action.button('停止输出', on_click=end_chat_streaming, help="点击此按钮停止流式输出")


# 用户输入响应，如果上一条消息不是助手的消息，且上一条用户消息还没有处理完毕
if (page_state.messages[-1]["role"] != "assistant"
        and not page_state.last_user_msg_processed):
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 检索知识库
            kmsg = ""
            if collection_value not in "":
                kmsg = search_knowledge(collection_value, page_state.chat_prompt)
            if kmsg != "":
                st.expander("📚 知识库检索结果", expanded=False).markdown(kmsg)
            sysmsg = get_ta365_sysmsg(kmsg)
            response = openai_streaming(sysmsg, page_state.messages[-10:])
            # 流式输出
            placeholder = st.empty()
            full_response = ''
            for item in response:
                # 如果用户手动停止了流式输出，就退出循环
                if page_state.streaming_end:
                    break
                text = item.content
                if text is not None:
                    full_response += text
                    placeholder.markdown(full_response)
                    page_state.update_last_msg("messages", {"role": "assistant", "content": full_response})
            placeholder.markdown(full_response)

    stop_action.empty()
    end_chat_streaming()
    st.rerun()


