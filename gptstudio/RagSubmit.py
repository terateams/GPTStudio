from dotenv import load_dotenv

from common.session import PageSessionState

load_dotenv()
import json
import os
from datetime import UTC, datetime
import tempfile

import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from common.azure_blob import upload_blobfile
from common.utils import md5hash

from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import Document
import concurrent.futures
import asyncio

from common.openai import openai_generate_vector

state = PageSessionState("rag_submit")
state.initn_attr("submit_names", [])

SERVICE_URL = "https://aita-search-pro.search.windows.net"
APIKEY = os.getenv("AZURE_SEARCH_API_ADMIN_KEY")


def upload_ragfile(filename, filepath):
    url = asyncio.run(
        upload_blobfile("ragfiles", filename, filepath, expiry_hours=24 * 30 * 10)
    )
    return url


# 分割文档为片段
# @st.cache_data(persist="disk")
def split_docs_with_llama(uploaded_file):
    # 将文件内容加载为文档对象
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())

    with open(temp_filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # 构造文档对象
    document = Document(text=content)

    # 使用 TokenTextSplitter 分割文档
    text_splitter = TokenTextSplitter(
        chunk_size=2048, chunk_overlap=64
    )  # 智能拆分，最大2048
    split_docs = text_splitter.split_text(document.get_content())

    parent_id = md5hash(temp_filepath)
    ragfilename = f"{parent_id}.txt"
    with st.spinner("正在上传文件..."):
        url = upload_ragfile(ragfilename, temp_filepath)

    json_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {
            executor.submit(openai_generate_vector, chunk): i
            for i, chunk in enumerate(split_docs)
        }
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]
            try:
                vector = future.result()
                json_data.append(
                    {
                        "parent_id": parent_id,
                        "chunk_id": md5hash(split_docs[i]),
                        "content": split_docs[i],
                        "filepath": ragfilename,
                        "url": url,
                        "contentVector": vector,
                    }
                )
            except Exception as exc:
                raise

    return json_data


def validate_single_object(data):
    """验证单条数据是否符合规范"""
    required_fields = ["chunk_id", "parent_id", "content", "contentVector"]

    for field in required_fields:
        if field not in data:
            return False, f"缺少必需字段: {field}"

    return True, "JSON 数据有效"


def get_search_client(index_name):
    """获取 Azure Search 客户端"""
    credential = AzureKeyCredential(APIKEY)
    return SearchClient(
        endpoint=SERVICE_URL, index_name=index_name, credential=credential
    )


def submit_to_azure_search(index_name, data):
    """提交数据到 Azure Search"""
    try:
        search_client = get_search_client(index_name)
        result = search_client.upload_documents(documents=data)

        if len(result) > 0 and all(res.succeeded for res in result):
            return True, "所有数据成功上传"
        errors = [res.error_message for res in result if not res.succeeded]
        return False, f"上传失败: {errors}"

    except Exception as e:
        return False, str(e)


def main():
    uploaded_files = st.file_uploader(
        "上传文本文件", type=["txt", "markdown"], accept_multiple_files=True
    )
    with st.sidebar:
        st.markdown("## 上传 RAG 数据")
        index_name = st.selectbox(
            "选择索引",
            [
                "aita-index",
                "tagpt4o-index",
                "ta10-index",
                "ta900-index",
                "ta1010-index",
                "ta2010-index",
                "ta189-index",
                "ta365-index",
            ],
        )
        submit_button = st.button("提交数据", key="submit_rag_parse")
        json_datas = []

    if submit_button and uploaded_files is not None:
        if index_name is None:
            st.error("请选择一个索引")
            return

        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
            if uploaded_file.name in state.submit_names:
                st.write(f"文件已经提交过了: {uploaded_file.name}")
                continue

            with st.spinner(f"正在解析 {filename}..."):
                try:
                    json_datas = split_docs_with_llama(uploaded_file)
                    st.write(f"文件{filename}已成功解析！")
                except Exception as e:
                    st.error(f"文件{filename}解析失败: {str(e)}")
                    return

            with st.spinner(f"正在提交 {filename}..."):
                success, response = submit_to_azure_search(index_name, json_datas)
                if success:
                    st.write(f"{filename} 数据已成功提交到 Azure AiSearch！")
                    state.submit_names.append(filename)
                else:
                    st.error(f"{filename} 提交失败:  {response}")


main()
