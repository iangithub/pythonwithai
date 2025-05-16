from ollama import generate

model = "llama3.2:3b"
prompt = """
請簡短描述一下台北101。
"""

# 指定模型版本與prompt
response = generate(
    model=model,prompt=prompt,
    options={'temperature': 0.5, 'num_predict': 200}
    )

# 輸出結果
print(response['response'])
