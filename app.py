import streamlit as st
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs API endpoint base URL
base_url = "https://api.elevenlabs.io/v1/text-to-speech"

# Default voice ID (Adam pre-made voice)
default_voice_id = "pNInz6obpgDQGcFmaJgB"

# Headers for the HTTP request
headers = {
    "Accept": "audio/mpeg",
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

def text_to_speech(text: str, voice_id: str = default_voice_id) -> BytesIO:
    url = f"{base_url}/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        audio_stream = BytesIO(response.content)
        return audio_stream
    else:
        st.error(f"Failed to generate speech: {response.status_code} - {response.text}")
        return None

def main():
    st.title("Text to Speech with ElevenLabs")

    st.write("## Enter Voice Description and Text")
    voice_description = st.text_input("Voice Description", "Default Voice (Adam)")
    text_input = st.text_area("Text to Convert to Speech", "Hello, this is a test.")

    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            audio_stream = text_to_speech(text_input)
            if audio_stream:
                st.audio(audio_stream, format="audio/mpeg")
                st.success("Audio generated successfully!")

if __name__ == "__main__":
    main()
