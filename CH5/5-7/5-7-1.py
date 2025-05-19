from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

speech_file_path = Path(__file__).parent / "speech.mp3"
with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="這是一段測試語音合成的文字。",
) as response:
    response.stream_to_file(speech_file_path)