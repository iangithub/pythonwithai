from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)

system_prompt = "你是一個專業且樂於助人的軟體工程師。"
user_prompt = "請用 Python 寫一個 two sum 的函數，給定一個整數陣列和一個目標值，返回兩個數字的索引。"

messages = [
    {"role": "system", "content": system_prompt},  
    {"role": "user", "content": user_prompt}       
]

response = client.chat.completions.create(
    model="o4-mini",
    messages=messages,
    reasoning_effort="low",
)


assistant_reply = response.choices[0].message.content
print("o4-mini 回答內容：\n", assistant_reply)

## 印出完整的回應內容
print("o4-mini 回答內容：\n", response.model_dump())