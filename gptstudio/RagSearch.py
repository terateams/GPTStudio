import json
import random
from typing import Any, Dict, List
from dotenv import load_dotenv

from common.session import PageSessionState

load_dotenv()
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from common.openai import openai_text_generate, openai_json_generate
from common.models import ExamRecord, get_db_session, get_exam_ignore_ids
from common import models, ExamCategorys
import os

SERVICE_URL = "https://aita-search-pro.search.windows.net"
APIKEY = os.getenv("AZURE_SEARCH_API_ADMIN_KEY")


def get_search_client(index_name):
    credential = AzureKeyCredential(APIKEY)
    return SearchClient(
        endpoint=SERVICE_URL, index_name=index_name, credential=credential
    )


def search_questions(index_name, search_text="", top=10, skip=0):
    client = get_search_client(index_name)

    # 构建过滤条件
    filter_conditions = []
    filter_expr = " and ".join(filter_conditions) if filter_conditions else None

    # 执行搜索
    results = client.search(
        search_text=search_text,
        filter=filter_expr,
        select=[
            "parent_id",
            "chunk_id",
            "content",
            "filepath",
            "url",
        ],
        query_type="semantic",  # 使用语义搜索
        semantic_configuration_name="default",
        # order_by=["filepath asc"],
        top=top,
        skip=skip,
    )

    # 将结果转换为列表
    results_list = list(results)
    return results_list


def main():
    with st.sidebar:
        st.markdown("## 检索 RAG 数据")
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
        search_text = st.text_input("输入检索关键字", "")
        search_button = st.button("检索数据", key="search_rag")
        
    if search_button:
        with st.spinner("正在检索数据..."):
            results = search_questions(index_name, search_text)
            for result in results:
                st.markdown(f"**{result['chunk_id']}**")
                st.markdown(f"{result['url']}")
                st.markdown(result["content"])
                st.divider()


main()