from ollama import generate

model = "llama3.2:3b"
prompt = """
你是一位暢銷偵探小說的作家，具有10年的創作經驗，正在撰寫一本新作，內容是一名敏銳的偵探，在午夜的懸疑現場，街上下著大雨，而你正為一起命案進行搜證。
請用200字以內描述現場氛圍與線索。
文字必須使用繁體中文。
"""

# 指定模型版本與prompt,並設定生成參數options
response = generate(model, prompt,options={'temperature': 0.7, 'num_predict': 200,'top_k': 50})

# 輸出結果
print("模型生成的創作內容：")
print(response.response)




# chat版本
from ollama import chat

# 初始化對話列表，包含一條 system 訊息設定模型角色
messages = [
    {"role": "system", "content": "你是一位暢銷偵探小說的作家，具有10年的創作經驗。"}  # 設定模型的角色或行為
]

# 使用者提出第一個問題
prompt = """
你正在撰寫一本新作，內容是一名敏銳的偵探，在午夜的懸疑現場，街上下著大雨，而你正為一起命案進行搜證。
請用200字以內描述現場氛圍與線索。
文字必須使用繁體中文。
"""
messages.append({"role": "user", "content": prompt})

# 指定模型版本與prompt,並設定生成參數options
response = chat(model, messages,options={'temperature': 0.7, 'num_predict': 200,'top_k': 50})

# 輸出結果
print("模型生成的創作內容：")
print(response.message.content)