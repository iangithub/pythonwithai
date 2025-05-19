from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

response = client.embeddings.create(
    input = "你好世界",
    model= "text-embedding-3-small"
)

print(len(response.data[0].embedding)) # 1536 維

response = client.embeddings.create(
    input = "你好世界",
    model= "text-embedding-3-small",
    dimensions=512
)

print(len(response.data[0].embedding)) # 512 維


