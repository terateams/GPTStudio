from dotenv import load_dotenv
load_dotenv()
import uuid

import streamlit as st
from st_audiorec import st_audiorec
from openai import OpenAI
from pydub import AudioSegment
from datetime import timedelta
from common.utils import get_global_datadir
from common.speech import audio_segment_split, generate_openai_transcribe
from common.openai import openai_text_generate
from hashlib import md5
import io
import sys
import os
import srt
from common.session import PageSessionState

st.sidebar.title("🔊 语音创作 ✨")

page_state = PageSessionState("speech")
# 用于存储临时文件
audio_tempdir = get_global_datadir("temp_audio")
page_state.initn_attr("input_type", "microphone")
page_state.initn_attr("audio_text_source", None)
page_state.initn_attr("recode_text", None)
page_state.initn_attr("latest_custom_file", None)

st.markdown(
    """
    <style>
    /* Target code blocks */
    .stCodeBlock > div {
        white-space: pre-wrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(persist="disk")
def get_speech(filename, language: str = "en"):
    return generate_openai_transcribe(filename, language, format="text")


def get_speech_text(audio_path, language):
    basename = os.path.basename(audio_path)
    audio_format = basename.split(".")[-1]
    audio_segment = AudioSegment.from_file(audio_path, format=audio_format)
    segs = audio_segment_split(audio_segment, 120)
    page_state.recode_text = ""
    for seg in segs:
        md5hash = md5(seg.raw_data).hexdigest()
        seg_audio_path = os.path.join(audio_tempdir, md5hash + ".mp3")
        seg.export(seg_audio_path, format="mp3")
        text = get_speech(seg_audio_path, language)
        page_state.recode_text += "\n" + text
    return page_state.recode_text

with st.sidebar:
    language = st.selectbox("选择源语言", ["zh", "en"], index=0)

wav_audio_recode = None
audio_path = None


tab1, tab2 = st.tabs(["录制语音", "上传音频"])

with tab1:
    wav_audio_recode = st_audiorec()
    if st.button("识别语音", key="do_recode"):
        if wav_audio_recode is not None:
            status = st.status("正在识别录制语音....", state="running", expanded=True)
            with status:
                status.update(label="正在保存语音....")
                _filename = md5(wav_audio_recode[:100]).hexdigest()
                # _filename = uuid.uuid4().hex
                audio_segment = AudioSegment.from_wav(io.BytesIO(wav_audio_recode))
                audio_path = os.path.join(audio_tempdir, f"{_filename}.audio.wav")
                audio_segment.export(audio_path, format="wav")
                status.update(label="已保存语音， 正在识别....")
                result = get_speech_text(audio_path, language)
                status.update(label="识别完成", state="complete")
        else:
            st.warning("没有录制到语音")

with tab2:
    uploaded_file = st.file_uploader(
        "上传音频文件", type=["wav", "mp3", "mp4", "ogg", "m4a"]
    )
    if uploaded_file:
        audio_path = os.path.join(audio_tempdir, os.path.basename(uploaded_file.name))
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.audio(audio_path)

    if audio_path and st.button("识别语音", key="do_uploadfile"):
        with st.spinner("正在识别上传语音...."):
            result = get_speech_text(audio_path, language)


st.divider()

if page_state.recode_text:
    st.code(page_state.recode_text)


if st.sidebar.button("清除历史数据", type="secondary"):
    page_state.recode_text = None
    st.rerun()
    