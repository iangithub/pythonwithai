from openai import OpenAI
import requests
import json

client = OpenAI(
    api_key = "sk-xx",
)    

web_api = "https://koko-demo-api.azurewebsites.net/inventory/"  

messages = [
    {"role": "system", "content": "請你幫我找火雞肉飯的庫存"}
]

tools_json = [
    {
        "type": "function",
        "function": {
            "name": "Prod_Inventory",
            "description": "Find the inventory of a product",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "prod": {
                        "type": "string",
                        "description": "產品名稱",
                    }
                },
                "required": ["prod"],
                "additionalProperties": False
            }
        }
    }
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools_json,
    tool_choice="auto",  
)

print(completion)

arguments = completion.choices[0].message.tool_calls[0].function.arguments
print("模型要呼叫 Tool 的參數：", arguments)

response = requests.get(web_api, params=json.loads(arguments))
api_result = response.json()
print("API 回傳結果：", api_result)


messages_2nd = messages + [
    {
        "role": "system",
        "content": f"庫存查詢結果：產品「{api_result['prod']}」目前庫存為 {api_result['inventory']} 個。"
    }
]


completion_2nd= client.chat.completions.create(
    model="gpt-4o",
    messages=messages_2nd
)

print(completion_2nd.choices[0].message.content)