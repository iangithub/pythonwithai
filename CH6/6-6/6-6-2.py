import requests
from io import BytesIO
from openai import OpenAI


client = OpenAI(
    api_key = "sk-xx",
)    

def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id

file_id = create_file(client, "https://cdn.openai.com/API/docs/deep_research_blog.pdf")

vector_store = client.vector_stores.create(
    name="my_knowledge"
)

vector_store_id = vector_store.id

print(vector_store_id)

result = client.vector_stores.files.create(
    vector_store_id=vector_store_id,
    file_id=file_id
)
print(result)

result = client.vector_stores.files.list(
    vector_store_id=vector_store_id
)
print(result)


response = client.responses.create(
    model="gpt-4o-mini",
    input="OpenAI 的  deep research 是什麼？?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [ vector_store_id]
    }]
)
print(response)