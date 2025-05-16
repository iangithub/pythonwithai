from ollama import generate

model = "llama3.2:3b"
prompt = """
你是一位暢銷偵探小說的作家，具有10年的創作經驗，正在撰寫一本新作，內容是一名敏銳的偵探，在午夜的懸疑現場，街上下著大雨，而你正為一起命案進行搜證。
請用200字以內描述現場氛圍與線索。
文字必須使用繁體中文。
"""

# 指定模型版本與prompt
response = generate(model, prompt)

# 輸出結果
print("模型生成的創作內容：")
print(response.response)
