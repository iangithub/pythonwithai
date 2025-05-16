from ollama import chat

model = "llama3.2:3b"

# 與模型對話
response = chat(
    model=model,
    messages=[{
        'role': 'user',
        'content': '解釋一下什麼是LLM模型的幻覺現象'
    }]
)

# 輸出結果
print(response['message']['content'])
