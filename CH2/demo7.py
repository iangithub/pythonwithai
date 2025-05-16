from ollama import generate
from pydantic import BaseModel

model = "llama3.2:3b"
prompt = """
買了書花了588元。
"""

class Product(BaseModel):
  name: str
  price: int


# 指定模型版本與prompt
response = generate(model, 
                    prompt,
                    format=Product.model_json_schema())

# 輸出結果
print("模型生成的內容：")
print(response.response)


