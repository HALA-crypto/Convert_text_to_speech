import streamlit as st
import edge_tts
import asyncio
import io
st.title("Convert Text to Speech")
text=st.text_area("Enter text to convert to speech")
language=st.selectbox("Select language",["عربي","English"])
VOICES = {
    "عربي": {
        
        " زارية (امرأة - السعودية)": "ar-SA-ZariyahNeural",
        " فهد (رجل - السعودية)":     "ar-SA-FahdNeural",
        " محمد (رجل - مصر)":         "ar-EG-ShakirNeural",
        " سلمى (امرأة - مصر)":       "ar-EG-SalmaNeural",
    },
    "English": {
        " Jack (Male - USA)":       "en-US-GuyNeural",
        " Jenny (Female - USA)":    "en-US-JennyNeural",
        " Ryan (Male - UK)":   "en-GB-RyanNeural",
        " Lily (Female - UK)": "en-GB-LibbyNeural",
    },
}
voice=st.selectbox("Select voice",list(VOICES[language].keys()))
voice_id=VOICES[language][voice]
async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks) 
if st.button("Generate Audio"):
    if text:
        audio_bytes = asyncio.run(generate_audio(text, voice_id))
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Please enter some text to convert to speech.")