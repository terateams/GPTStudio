import base64
import uuid
from dotenv import load_dotenv
import os

from common.openai import openai_analyze_image
from common.session import PageSessionState
load_dotenv()
import streamlit as st
import io
from streamlit_paste_button import paste_image_button as pbutton
from common.utils import get_global_datadir
from common.azure_blob import upload_blobfile
import asyncio

# Specify your desired directory
save_dir = get_global_datadir("pasted_images")
os.makedirs(save_dir, exist_ok=True)


page_state = PageSessionState("imagetools")
page_state.initn_attr("image_url", "")
page_state.initn_attr("image_text", "")

async def upload_image(imgid, filepath):
    url = await upload_blobfile("exam-images", f"{imgid}.png", filepath, expiry_hours=24 * 30 * 10)

    # st.image(url)

paste_result = pbutton("📋 粘贴图片")
            
if paste_result.image_data:
    # Display the image
    st.image(paste_result.image_data, width=360)
    
    if st.button("上传至 Azure Blob", key="upload_image"):
        # Save image to specified directory
        imgid = str(uuid.uuid4())
        file_path = os.path.join(save_dir, f"{imgid}.png")
        paste_result.image_data.save(file_path, format="PNG")
        # Optionally display the saved path
        st.write(f"图片已保存至: {file_path}")
        with st.spinner("正在上传图片至 Azure Blob..."):
            image_url =asyncio.run(upload_image(imgid, file_path))
            if image_url:
                page_state.image_url = image_url
        
    if page_state.image_url:
        st.code(page_state.image_url, language="text", wrap_lines=True)

    if st.button("识别内容"):
        img_bytes = io.BytesIO()
        paste_result.image_data.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()  # Image as bytes
        # Convert to base64
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")  # Image as base64
        with st.spinner("正在识别图片内容..."):
            prompt = "请识别图中的内容到 markdown 格式"
            text_result = openai_analyze_image(
                prompt, model="gpt-4o", imageb64=img_b64
            )
            if text_result:
                page_state.image_text = text_result
                
    if page_state.image_text:
        st.code(page_state.image_text, language="markdwon", wrap_lines=True)