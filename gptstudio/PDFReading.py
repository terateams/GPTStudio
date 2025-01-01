import zipfile
from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import tempfile
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from common.utils import md5hash, file_hash

# Azure Form Recognizer 配置
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

if "markdown_content" not in st.session_state:
    st.session_state.markdown_content = ""

if "markdown_content_files" not in st.session_state:
    st.session_state.markdown_content_files = []
    
st.title("PDF 文档分割与识别")

def split_pdf(input_file, start_page, pages_per_split=3, stbox=None):
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    split_num = 1

    # 创建子目录
    basename = os.path.basename(input_file)
    output_dir = os.path.join(tempfile.gettempdir(), f"{basename[:-4]}_splits")
    os.makedirs(output_dir, exist_ok=True)

    while start_page <= total_pages:
        writer = PdfWriter()
        end_page = start_page + pages_per_split - 1
        for i in range(start_page - 1, min(end_page, total_pages)):
            writer.add_page(reader.pages[i])
        
        output_file = os.path.join(output_dir, f"{basename[:-4]}-{split_num:03d}.pdf")
        with open(output_file, 'wb') as out_file:
            writer.write(out_file)
        
        stbox.success(f"创建: {output_file}")
        
        start_page += pages_per_split
        split_num += 1

    stbox.success(f"文件已分割完成！分割总数: {split_num - 1}")
    return output_dir

@st.cache_data(show_spinner=True, persist=True)
def analyze_document(file_path):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document("prebuilt-read", f)
        result = poller.result()
    
    lines = []
    for page in result.pages:
        for line in page.lines:
            lines.append(line.content)
    return "\n".join(lines)
    # return result.content
    
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("上传 PDF 文件", type=["pdf"])

    if uploaded_file is not None:
        tmppath = os.path.join(tempfile.gettempdir(), "learnzy-files")
        os.makedirs(tmppath, exist_ok=True)
        with open(os.path.join(tmppath, f"{md5hash(uploaded_file.name)}.pdf"), "wb") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        st.success("文件上传成功！")

        # 分割 PDF 文件
        stbox = st.empty()
        with st.spinner("正在处理文档文件..."):
            output_dir = split_pdf(temp_file_path, start_page=1, pages_per_split=3,stbox=stbox )

        # 识别并合并内容
        mdbox = col2.empty()
        for file_name in sorted(os.listdir(output_dir)):
            if not file_name.endswith(".pdf"):
                continue
            with st.spinner(f"正在识别 PDF 文件 ({file_name}) 内容..."):
                file_path = os.path.join(output_dir, file_name)
                content = analyze_document(file_path)
                st.session_state.markdown_content += f"\n\n{content}\n\n"
                mdbox.code(content, language="markdown")
                
                text_file_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.txt")
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(content)
                st.session_state.markdown_content_files.append(text_file_path)

        # 显示合并后的内容
        if st.session_state.markdown_content:
            st.success("PDF 文件识别完成！")
            
        
        # 增加按钮，将所有片段保存为独立文件并压缩为 ZIP 文件
        if st.button("下载 >>"):
            st.download_button(
                label="下载合并后的内容",
                data=st.session_state.markdown_content,
                file_name="merged_content.md",
                mime="text/markdown",
            )
            basename = os.path.basename(temp_file_path)
            zip_output_path = os.path.join(tempfile.gettempdir(), f"{os.path.splitext(basename)[0]}_splits.zip")
            with zipfile.ZipFile(zip_output_path, 'w') as zipf:
                top_level_dir = os.path.splitext(basename)[0] + "_splits"
                for text_file in st.session_state.markdown_content_files:
                    zipf.write(text_file, arcname=os.path.join(top_level_dir, os.path.basename(text_file)))
            with open(zip_output_path, "rb") as zip_file:
                st.download_button(
                    label="合并的 ZIP 文件",
                    data=zip_file.read(),
                    file_name=f"{os.path.splitext(basename)[0]}_splits.zip",
                    mime="application/zip",
                )


