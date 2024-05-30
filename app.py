import streamlit as st
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
from voice_descriptions import get_voices

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs API endpoint base URLs
base_url = "https://api.elevenlabs.io/v1"
tts_url = f"{base_url}/text-to-speech"
sts_url = f"{base_url}/speech-to-speech"  # Add the speech-to-speech endpoint

# Default voice ID (Adam pre-made voice)
default_voice_id = "pNInz6obpgDQGcFmaJgB"

# Headers for the HTTP request
headers = {
    "Accept": "audio/mpeg",
    "xi-api-key": ELEVENLABS_API_KEY,
}

# In-memory storage for audio files
audio_files = []

def text_to_speech(text: str, voice_id: str = default_voice_id) -> BytesIO:
    url = f"{tts_url}/{voice_id}"
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

def speech_to_speech(audio_file, voice_id: str = default_voice_id) -> BytesIO:
    url = f"{sts_url}/{voice_id}"
    files = {
        'audio': audio_file
    }
    response = requests.post(url, headers=headers, files=files)

    if response.ok:
        audio_stream = BytesIO(response.content)
        return audio_stream
    else:
        st.error(f"Failed to generate speech: {response.status_code} - {response.text}")
        return None

def save_audio(audio_stream, filename):
    with open(filename, 'wb') as f:
        f.write(audio_stream.getbuffer())
    return filename

def main():
    st.title("Text to Speech and Speech to Speech with ElevenLabs")

    st.write("## Enter Voice Description and Text")
    voices = get_voices()
    voice_options = {voice['name']: voice['voice_id'] for voice in voices}
    voice_name = st.selectbox("Select a voice", options=list(voice_options.keys()))
    selected_voice_id = voice_options[voice_name]
    
    text_input = st.text_area("Text to Convert to Speech", "Hello, this is a test.")

    if st.button("Generate Audio"):
        with st.spinner("Generating audio..."):
            audio_stream = text_to_speech(text_input, voice_id=selected_voice_id)
            if audio_stream:
                filename = f"audio_{len(audio_files) + 1}.mp3"
                save_audio(audio_stream, filename)
                audio_files.append(filename)
                st.audio(audio_stream, format="audio/mpeg")
                st.download_button(label="Download Audio", data=audio_stream.getvalue(), file_name=filename, key=filename)
                st.success(f"Audio generated and saved as {filename}!")

    st.write("## Upload an Audio Clip")
    uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])
    if uploaded_file is not None:
        if st.button("Generate Voice from Clip"):
            with st.spinner("Generating audio from clip..."):
                audio_stream = speech_to_speech(uploaded_file, voice_id=selected_voice_id)
                if audio_stream:
                    filename = f"audio_{len(audio_files) + 1}.mp3"
                    save_audio(audio_stream, filename)
                    audio_files.append(filename)
                    st.audio(audio_stream, format="audio/mpeg")
                    st.download_button(label="Download Audio", data=audio_stream.getvalue(), file_name=filename, key=filename)
                    st.success(f"Audio generated and saved as {filename}!")

    st.write("## Previously Generated Audios")
    for i, audio_file in enumerate(audio_files):
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
            st.audio(audio_file, format="audio/mpeg")
            st.download_button(label="Download Audio", data=audio_data, file_name=audio_file, key=f"download_{i}")

    st.write("## Available Voices and Descriptions")
    if voices:
        for voice in voices:
            st.write(f"**Name**: {voice['name']}")
            st.write(f"**Voice ID**: {voice['voice_id']}")
            # Display additional details if available
            st.write(f"**Description**: {voice.get('description', 'No description available')}")
            if 'gender' in voice:
                st.write(f"**Gender**: {voice['gender']}")
            if 'language' in voice:
                st.write(f"**Language**: {voice['language']}")
            st.write("---")

if __name__ == "__main__":
    main()
