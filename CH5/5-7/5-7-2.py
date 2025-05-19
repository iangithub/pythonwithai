from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

speech_file_path = Path(__file__).parent / "speech.mp3"
audio_file = open(speech_file_path, "rb")

transcript = client.audio.transcriptions.create(
    model="gpt-4o-transcribe",
    file=audio_file,
    prompt="請使用正體中文進行轉錄。",
)

print(transcript.text)
