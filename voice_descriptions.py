import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs API endpoint for voices
voices_url = "https://api.elevenlabs.io/v1/voices"

# Headers for the HTTP request
headers = {
    "Accept": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

def get_voices():
    response = requests.get(voices_url, headers=headers)
    if response.ok:
        return response.json()['voices']
    else:
        print(f"Failed to fetch voices: {response.status_code} - {response.text}")
        return []
