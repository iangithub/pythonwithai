from ollama import generate

model = "llama3.2:3b"
prompt = """
請為一個關於現代職場冒險的故事撰寫大綱。
故事主角是一位剛畢業的大學生，勇於捍衛自身權益，他該如何在充滿人性挑戰的現實職場上，走出屬於自已道路。
"""

# 指定模型版本與prompt
response = generate(model, prompt)

# 輸出結果
print(response['response'])
