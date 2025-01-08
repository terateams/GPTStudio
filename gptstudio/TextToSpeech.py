from dotenv import load_dotenv

load_dotenv()
import streamlit as st
from pydub import AudioSegment
from common.session import PageSessionState
from common.speech import (
    generate_azure_speech_segment,
    generate_openai_speech_segment,
)


state = PageSessionState("text_to_speech")
state.initn_attr("speech_text", "")

st.title("🎙️ 文本转语音")
col1, col2 = st.columns([1, 2])

with col1:
    param_box = st.container()
    state.speech_type = param_box.selectbox("Speech type", ["azure", "openai"], index=0)
    if state.speech_type == "azure":
        state.language = st.selectbox("语言", ["en-US", "zh-CN"], index=0)
        state.speech_voice = param_box.selectbox(
            "azure voice",
            [
                "en-US-EmmaMultilingualNeural",
                "en-US-AndrewMultilingualNeural",
                "en-US-AvaMultilingualNeural",
                "en-US-BrianMultilingualNeural",
                "en-US-JennyMultilingualNeural",
                "zh-CN-YunxiNeural",
                "zh-CN-YunjianNeural",
                "zh-CN-YunyangNeural",
                "zh-CN-YunfengNeural",
                "zh-CN-YunhaoNeural",
                "zh-CN-YunxiaNeural",
                "zh-CN-YunyeNeural",
                "zh-CN-YunzeNeural",
                "zh-CN-XiaoyiNeural",
                "zh-CN-XiaochenNeural",
                "zh-CN-XiaohanNeural",
                "zh-CN-XiaoxiaoNeural",
                "zh-CN-XiaomengNeural",
                "zh-CN-XiaomoNeural",
                "zh-CN-XiaoqiuNeural",
                "zh-CN-XiaoruiNeural",
                "zh-CN-XiaoshuangNeural",
                "zh-CN-XiaoxuanNeural",
                "zh-CN-XiaoyanNeural",
                "zh-CN-XiaoyouNeural",
                "zh-CN-XiaozhenNeural",
            ],
            index=0,
        )
        state.speech_speed = None
    else:
        state.speech_voice = param_box.selectbox(
            "openai voice",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            index=0,
        )
        state.speech_speed = param_box.slider(
            "Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1
        )
    ttl_button = st.button("生成")


@st.cache_data
def st_generate_speech_segment(
    text: str, voice: str, language: str = "en_US", speed: float = 1.0
) -> AudioSegment:
    if state.speech_type == "azure":
        return generate_azure_speech_segment(text, "en_US", voice)
    elif state.speech_type == "openai":
        return generate_openai_speech_segment(text, voice, speed=speed)


with col2:
    srt_text = st.text_area("文本内容", state.speech_text, height=270)
    if srt_text:
        state.speech_text = srt_text

    audio_box = st.container()

    if ttl_button:
        with st.spinner("生成中..."):
            # 合并音频段
            merged_audio = st_generate_speech_segment(
                state.speech_text,
                state.speech_voice,
                state.language,
                state.speech_speed,
            )
            if merged_audio is None:
                st.error("生成音频失败！")
                st.stop()

            # 导出为文件
            merged_audio_path = "text_to_speech_final_audio.mp3"
            merged_audio.export(merged_audio_path, format="mp3")

            # 提供下载链接
            audio_box.audio(merged_audio_path)
            audio_box.download_button(
                label="下载音频",
                data=open(merged_audio_path, "rb"),
                file_name="final_audio.mp3",
                mime="audio/mp3",
            )
