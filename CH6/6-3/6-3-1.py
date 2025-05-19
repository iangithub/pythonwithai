from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

code = """
class Inventory {
  prod: string = "";
  inventory: string = "";
  manager: string = "";
}

export default Inventory;
"""

refactor_prompt = """
用 email 來取代 manager 的欄位，只回應程式碼，不要有任何解釋，不要有 markdown 語法。
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": refactor_prompt
        },
        {
            "role": "user",
            "content": code
        }
    ],
    prediction={
        "type": "content",
        "content": code
    }
)

print(completion)
print(completion.choices[0].message.content)