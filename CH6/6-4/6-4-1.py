from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

inputs = [
    {
        "type": "text",
        "text": "我恨所有跟我不同信仰的人，應該都去死。"
    },
    {
        "type": "image_url",
        "image_url": {
            "url": "請自己從色情網址上找一張圖片，然後把網址貼在這裡，本書不便提供"
        }
    }
]

response = client.moderations.create(
    model="omni-moderation-latest",
    input=inputs
)

print(response.model_dump_json(indent=2))
