from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    api_key = "sk-xx",
)    

class Inventory(BaseModel):
    prod: str
    inventory: int

messages = [
    {
        "role": "user",
        "content": "火雞肉飯的庫存還有十個"
    },

]

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    response_format=Inventory
)

inventory_content = response.choices[0].message.content

print("choices[0].message.content：", inventory_content)

inventory_parsed = response.choices[0].message.parsed

print(inventory_parsed)
print(type(inventory_parsed))