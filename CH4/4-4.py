import base64
import json
import os
import random
import boto3

client = boto3.client("bedrock-runtime")
model_id = "amazon.nova-canvas-v1:0"

# 輸入要產出圖片的提示
prompt = "一個台灣女生在路邊攤吃蚵仔煎。"
# prompt = """
# 台灣女生坐在路邊的小吃攤的椅子上，
# 吃一道以新鮮蚵仔肉、澱粉以及蛋煎炸而成的小吃，
# 通常搭配酸辣味的醬料一同食用。"
# """
# Generate a random seed between 0 and 858,993,459
seed = random.randint(0, 858993460)

# 圖像生成參數設定
native_request = {
    "taskType": "TEXT_IMAGE",
    "textToImageParams": {"text": prompt},
    "imageGenerationConfig": {
        "seed": seed,
        "quality": "standard",
        "height": 512,
        "width": 512,
        "numberOfImages": 1,
    },
}

# 呼叫API產生圖像
request = json.dumps(native_request)
response = client.invoke_model(modelId=model_id, body=request)
model_response = json.loads(response["body"].read())
base64_image_data = model_response["images"][0]

# 確認是否有output資料夾，若無則建立
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
image_data = base64.b64decode(base64_image_data)
# 準備圖像檔案名稱
i = 1
while os.path.exists(os.path.join(output_dir, f"generated-{i}.png")):
    i += 1
image_path = os.path.join(output_dir, f"generated-{i}.png")
# 將圖像資料寫入檔案
with open(image_path, "wb") as file:
    file.write(image_data)
print(f"Image saved to {image_path}")
