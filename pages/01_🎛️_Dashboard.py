import streamlit as st
from urllib.parse import quote as urlencode

st.set_page_config(page_title="CoolStudy 应用面板", page_icon="🎛️")

st.sidebar.markdown("# 🎛️ 应用面板")

# List of apps
apps = [
    {
        "name": "📚 知识库搜索",
        "remark": "`TeamsGPT 知识库检索，输入主题，检索相关知识`",
        "link": urlencode("Knowledge_Search"),
    },
    {
        "name": "🌐 Radius RFC 搜索",
        "remark": "`RADIUS RFC 文档检索，输入主题，检索相关内容。`",
        "link": urlencode("Radius_RFC_Search"),
    },
    {
        "name": "🔬 图像分析",
        "remark": "`通过 AI 分析图像中的内容，提供有用的信息`",
        "link": urlencode("Image_Analysis"),
    },
    {
        "name": "✨ 智能思维导图",
        "remark": "`通过 AI 模型分析，生成智能思维导图`",
        "link": urlencode("AI_Mindmap"),
    },
    {
        "name": "🎙️ 语音转录",
        "remark": "`通过 AI 模型识别语音内容，转录文本，并支持合成新语音`",
        "link": urlencode("Speech_Transcribe"),
    },
    {
        "name": "💡 Ta365",
        "remark": "`博学多才的人工智能学习导师，可以帮助学生解决各种学习上的问题`",
        "link": urlencode("Ta365_Chatbot"),
    },
    {
        "name": "🐍 Python_编程导师",
        "remark": "`一个 Python 学习助手，可以设计学习计划、解答问题`",
        "link": urlencode("Codeboy"),
    },
    {
        "name": "🎨 图像生成",
        "remark": "`通过 AI 模型生成图像，包括人脸、动漫人物、风景等`",
        "link": urlencode("Image_Generation"),
    },
    {
        "name": "🎬 字幕语音合成",
        "remark": "`通过 AI 模型合成字幕中的语音内容, 支持多种音色`",
        "link": urlencode("Subtitles_To_Speech"),
    },
]

cols = st.columns(3)
# Iterating over the apps to create buttons in the UI
for i, app in enumerate(apps):
    # Determine which column to place the app based on index
    col = cols[i % 3]
    # Create a button for each app in the respective column
    with col.expander(app['name'], expanded=True):
        st.markdown(app['remark'])
        link = app['link']
        name = app['name']
        link_html = f"""
    <a href="{link}" target="_self" style="
        text-decoration: none;
        color: RoyalBlue;
        background-color: Gainsboro;
        padding: 7px 14px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        ">
    {name}
    </a>
"""
        st.markdown(link_html, unsafe_allow_html=True)

        # st.link_button(app['name'], app['link'])
