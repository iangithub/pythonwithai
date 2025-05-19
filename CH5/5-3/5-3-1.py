from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)

system_prompt = "你是一個專業且樂於助人的助理。"
user_prompt = "請解釋什麼是機器學習？"

messages = [
    {"role": "system", "content": system_prompt},  
    {"role": "user", "content": user_prompt}       
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    temperature=0.7,  
    max_tokens=100    
)

assistant_reply = response.choices[0].message.content
print("GPT-4o 回答內容：\n", assistant_reply)

## 印出完整的回應內容
print("GPT-4o 回答內容：\n", response.model_dump())