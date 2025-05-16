import boto3
import json

bedrock_runtime = boto3.client(service_name="bedrock-runtime")

user_input = "工作可以與興趣結合嗎？"

body = json.dumps(
    {
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": user_input}],
        "anthropic_version": "bedrock-2023-05-31",
    }
)

response = bedrock_runtime.invoke_model(
    body=body, modelId="anthropic.claude-3-haiku-20240307-v1:0"
)

response_body = json.loads(response.get("body").read())

print("User : ", user_input)
print("AI : ", response_body["content"][0]["text"])