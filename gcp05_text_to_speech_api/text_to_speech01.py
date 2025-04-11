import os
from pathlib import Path

from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import texttospeech

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

# Get file paths
file_path = Path(__file__).parent
input_path = file_path / "templates" / "ja.txt"
output_dir = file_path / "results"
output_path = output_dir / "ja.mp3"

# Create results directory if it doesn't exist
output_dir.mkdir(exist_ok=True)

# Read Japanese text from file
with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# Set up client options with API key
client_options = ClientOptions(api_key=api_key)

# Initialize the client with API key
client = texttospeech.TextToSpeechClient(client_options=client_options)

# Set the text to be converted
synthesis_input = texttospeech.SynthesisInput(text=text)

# Configure voice parameters - CORRECTED GENDER FOR JA-JP-NEURAL2-B
voice = texttospeech.VoiceSelectionParams(
    language_code="ja-JP", name="ja-JP-Neural2-B", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Select the audio file type (MP3)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Perform the text-to-speech conversion
response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

# The response's audio_content is binary (the MP3 file)
with open(output_path, "wb") as out:
    out.write(response.audio_content)
    print(f'音声コンテンツが "{output_path}" に保存されました')
