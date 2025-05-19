import json
import base64
import asyncio
import websockets
import aiohttp
import pyaudio
import signal
import sys

OPENAI_API_KEY = "sk-xx"

REALTIME_API_URL = "wss://api.openai.com/v1/realtime"

async def create_transcription_session():
    """
    呼叫 Realtime /transcription_sessions 端點，取得臨時 token，供後續 WebSocket 連線使用
    """
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        body = {
            "input_audio_format": "pcm16",  # 指定輸入音訊格式 (16-bit PCM)
            "input_audio_transcription": {
                "model": "gpt-4o-transcribe"
            },
            "turn_detection": {
                "type": "server_vad",      # 讓伺服器幫忙偵測語音開始/結束
                "silence_duration_ms": 800 # 靜音超過 800ms 即判斷一段話結束
            }
        }
        url = "https://api.openai.com/v1/realtime/transcription_sessions"
        resp = await session.post(url, headers=headers, json=body)
        if resp.status != 200:
            text = await resp.text()
            raise RuntimeError(f"創建轉錄會話失敗: {resp.status}, {text}")
        data = await resp.json()
        ephemeral_token = data["client_secret"]["value"]
        return ephemeral_token

async def realtime_transcription():
    """
    與 OpenAI Realtime API 建立 WebSocket 連線，並將麥克風音訊即時傳送給伺服器以轉錄文字。
    終端機會顯示即時轉錄結果。
    """
    ephemeral_token = await create_transcription_session()

    ws_headers = {
        "Authorization": f"Bearer {ephemeral_token}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(REALTIME_API_URL, extra_headers=ws_headers) as openai_ws:
        # 等待伺服器發來確認 (例如 transcription_session.created)
        ack = await openai_ws.recv()
        print("[Info] Transcription session created:", ack)

        audio = pyaudio.PyAudio()
        
        # 可依實際麥克風調整頻道/採樣率，此處示範 16kHz 單聲道 16-bit
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024 

        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        stream.start_stream()

        print("開始錄音，你說話後，終端機將即時顯示文字轉錄，按 Ctrl+C 結束。\n")

        # 建立並行的協程：一邊傳送音訊，一邊接收轉錄
        async def send_audio():
            while True:
                # 讀取一塊音訊資料
                audio_data = stream.read(CHUNK, exception_on_overflow=False)
                # base64 編碼
                audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                # 傳送 input_audio_buffer.append 事件
                event = {"type": "input_audio_buffer.append", "audio": audio_b64}
                await openai_ws.send(json.dumps(event))
                await asyncio.sleep(0.01)  # 略作延遲，避免壓力過大

        async def receive_transcripts():
            partial_text = ""
            async for raw in openai_ws:
                msg = json.loads(raw)
                etype = msg.get("type")
                if etype == "conversation.item.input_audio_transcription.delta":
                    # 收到部分轉錄文字
                    delta_text = msg.get("delta", "")
                    partial_text += delta_text
                    # 直接印在終端機（不換行）後 flush
                    sys.stdout.write(delta_text)
                    sys.stdout.flush()
                elif etype == "conversation.item.input_audio_transcription.completed":
                    # 一段話完整結束
                    final_text = msg.get("transcript", "")
                    # 在終端機換行
                    sys.stdout.write(f"\n[完整轉錄] {final_text}\n\n")
                    sys.stdout.flush()
                    partial_text = ""

                elif etype == "input_audio_buffer.speech_stopped":
                    # 伺服器偵測到靜音，代表一句話結束
                    pass
                elif etype == "error":
                    err = msg.get("error", "Unknown error")
                    print(f"\n[錯誤] {err}")
                    break

        # 利用 asyncio.gather 同時跑傳送/接收
        tasks = [
            asyncio.create_task(send_audio()),
            asyncio.create_task(receive_transcripts())
        ]
        
        # 透過信號或按 Ctrl+C 時可中斷
        # 下方是簡易中斷處理，讓程序結束時能停止錄音並關閉 websocket
        loop = asyncio.get_running_loop()
        stop_event = asyncio.Event()

        def handle_signal(sig, frame):
            print("\n[Info] 收到中斷訊號，準備結束...")
            stop_event.set()

        signal.signal(signal.SIGINT, handle_signal)

        await stop_event.wait()

        # 結束前關閉麥克風、WebSocket
        for t in tasks:
            t.cancel()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("錄音已關閉。")

async def main():
    await realtime_transcription()

if __name__ == "__main__":
    asyncio.run(main())
