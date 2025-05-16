from ollama import chat

model = "hf.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF:latest"


# 初始化對話歷史列表，包含 system 訊息設定模型身份
messages = [
    {"role": "system", "content": "你是一個友善且專業的 AI 專家，擅長用簡單白話的描述回答使用者有關AＩ的問題。"}  # 設定模型的角色或行為
]

# 使用者提出第一個問題
messages.append({"role": "user", "content": "現在的生成式AI與傳統AI有什麼不同？"})
response = chat(model=model, messages=messages)
answer = response.message.content
print("Assistant:", answer)

# 將模型的回答加入對話歷史
messages.append({"role": "assistant", "content": answer})

# 使用者提出第二個跟進問題
messages.append({"role": "user", "content": "會讓程式設計師失業嗎？"})
response = chat(model=model, messages=messages)
answer = response.message.content
print("Assistant:", answer)
