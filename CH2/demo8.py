from ollama import chat
from pydantic import BaseModel

model = "llama3.2:3b"

class Product(BaseModel):
    name: str
    price: int

# 初始化對話列表
messages = [
    {"role": "system", "content": "你是一個資料分析助手，請從使用者的描述中提取資訊，並用JSON格式回應。"}
]

# 使用者提問
user_message = "買了書花了588元。"
messages.append({"role": "user", "content": user_message})

# 使用chat函數並指定格式
response = chat(
    model=model,
    messages=messages,
    format=Product.model_json_schema()
)

# 輸出結果
print("模型生成的內容：")
print(response.message.content)