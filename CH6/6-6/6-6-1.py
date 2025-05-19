from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input="現在台北的天氣怎麼樣？",
)

print(response.output_text)