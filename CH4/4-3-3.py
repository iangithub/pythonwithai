# Call nova-micro model
import boto3
import json

client = boto3.client("bedrock-runtime")

MICRO_MODEL_ID = "us.amazon.nova-micro-v1:0"

# 系統提示訊息
system_list = [{"text": "你是一個職涯顧問。"}]

# 使用者問題
user_input = "工作可以與興趣結合嗎？"

# Define one or more messages using the "user" and "assistant" roles.
message_list = [{"role": "user", "content": [{"text": user_input}]}]

# 相關參數設定
inf_params = {"maxTokens": 4096, "topP": 0.9, "topK": 20, "temperature": 0.7}

request_body = {
    "schemaVersion": "messages-v1",
    "messages": message_list,
    "system": system_list,
    "inferenceConfig": inf_params,
}

response = client.invoke_model(modelId=MICRO_MODEL_ID, body=json.dumps(request_body))

response_body = json.loads(response.get("body").read())

print("User : ", user_input)
print("AI : ", response_body["output"]["message"]["content"][0]["text"])