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
GPTStudio is a library of tools based on GPT (Generative Pre-trained Transformer).
It is designed to provide developers and data scientists with powerful and easy-to-use GPT capabilities.
It combines knowledge base management, GPT capabilities, and a collection of AI-based tools to make it a powerful and easy-to-use tool for anyone involved in AI and big data.
making it ideal for any project involving AI and big models.

## Key Features

### Knowledge base retrieval:

Provides an efficient search tool to help users quickly find relevant information in the knowledge base.

### GPT Proficiency Test
- **Model Capability Testing**: Allows users to test the performance and capability of GPT models with the assistance of the knowledge base.
- **Real-time Feedback**: Provides real-time feedback to help users understand the response and accuracy of the model.

### AI Tools Collection
- **A wide range of AI tools**: including but not limited to text generation, language understanding, data analysis and many other AI-related tools.
- **Large Model Support**: Supports integration with other large AI models to extend the capability and scope of the application.

Translated with www.DeepL.com/Translator (free version)
""")


def main():
    """Main app"""
    show_page()


if __name__ == "__main__":
    main()
