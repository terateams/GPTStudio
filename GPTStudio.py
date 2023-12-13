import streamlit as st
from libs.msal import msal_auth

msal_auth()


def sidebar():
    st.sidebar.markdown("""
# 🦜GPTStudio
- [GPTStudio Github](https://github.com/terateams/GPTService)
- [Streamlit Website](https://streamlit.io)
    """)
    if st.sidebar.button('登出'):
        st.session_state['authenticated'] = False
        st.rerun()


def show_page():
    sidebar()
    st.title("🦜GPTStudio")
    st.markdown("""
GPTStudio 是一个基于 GPT 的工具库。它旨在为开发人员和数据科学家提供强大而易用的 GPT 功能。
它结合了知识库管理、GPT 功能和一系列基于人工智能的工具，使其成为人工智能和大数据相关人员的强大而易用的工具。
使其成为涉及人工智能和大模型的任何项目的理想选择。

### 关键功能

#### 知识库检索：

提供高效的搜索工具，帮助用户快速查找知识库中的相关信息。

#### GPT 能力测试
- **模型能力测试**： 允许用户在知识库的帮助下测试 GPT 模型的性能和能力。
- **实时反馈**： 提供实时反馈，帮助用户了解模型的响应和准确性。

#### 人工智能工具集
- **广泛的人工智能工具**：包括但不限于文本生成、语言理解、数据分析和许多其他人工智能相关工具。
- **大型模型支持**： 支持与其他大型人工智能模型集成，以扩展应用程序的能力和范围。

""")


def main():
    """Main app"""
    show_page()


if __name__ == "__main__":
    main()
