
from ollama import generate
from ollama import chat
import base64

model = "hf.co/second-state/Llava-v1.5-7B-GGUF:latest"

def encode_image(image_path: str) -> str:
    """ 將圖像轉為 Base64 格式 """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


image_data = encode_image("data/1.jpg")

# 調用多模態模型分析圖像
response = generate(
    model=model,
    prompt="分析一下這張圖片。",
    images=[image_data]
)
# 輸出結果
print("模型生成的內容：")
print(response.response)



# chat 對話版本
# 初始化對話列表
messages = [
    {"role": "user", "content": "分析一下這張圖片。", "images": [image_data]}
]

# 調用多模態模型分析圖像
response = chat(
    model=model,
    messages=messages
)

# 輸出結果
print("模型生成的內容：")
print(response.message.content)
