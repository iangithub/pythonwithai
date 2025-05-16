from ollama import generate

model = "llama3.2:3b"
prompt = """
你是一位暢銷偵探小說的作家，具有10年的創作經驗，正在撰寫一本新作，內容是一名敏銳的偵探，在午夜的懸疑現場，街上下著大雨，而你正為一起命案進行搜證。
請創作一則現代都市傳說的故事，字數500個字    
文字必須使用繁體中文。
"""

# 指定模型版本與prompt
response = generate(model, prompt,options={'temperature': 0.7, 'num_predict': 200,'top_k': 50}, stream=True)

# 串流式輸出結果
print("模型生成的創作內容：")
for chunk in response:
    print(chunk['response'], end='', flush=True)


# chat 對話模式的串流輸出
from ollama import chat

# 初始化對話列表，包含一條 system 訊息設定模型身份
messages = [
    {"role": "system", "content": "你是一位暢銷偵探小說的作家，具有10年的創作經驗。"}  # 設定模型的角色或行為
]

# 使用者提出第一個問題
prompt = """
你正在撰寫一本新作，內容是一名敏銳的偵探，在午夜的懸疑現場，街上下著大雨，而你正為一起命案進行搜證。
請創作一則現代都市傳說的故事，字數500個字    
文字必須使用繁體中文。
"""
messages.append({"role": "user", "content": prompt})

# 指定模型版本與prompt，以串流輸出：
print("模型生成的創作內容：")
for chunk in chat(model=model, messages=messages, options={'temperature': 0.7, 'num_predict': 200, 'top_k': 50}, stream=True):
    print(chunk['message']['content'], end='', flush=True)

