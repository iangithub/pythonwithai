from ollama import generate

model = "llama3.2:3b"
prompt = """
量子力學是一門描述微觀世界（如原子和次原子粒子）行為的物理學理論。它與我們日常生活中所接觸到的經典物理學不同，因為在量子層級上
"""

# 指定模型版本與prompt
response = generate(model, prompt)

# 輸出結果
print("模型生成的續寫內容：")
print(response.response)
