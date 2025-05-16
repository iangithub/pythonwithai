# 匯入Gemini API所需的程式庫
from google import genai
from google.genai import types
import json

# 實作生成函式
def generate(imageData):
    client = genai.Client(
        api_key="GEMINI_API_KEY"
    )

    model = "gemini-2.0-flash"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    data=imageData,
                    mime_type="image/jpeg",
                ),
                types.Part.from_text(text="""你是美食評論家，請根據這張圖片（無論是否為食物）給予一段正面的、鼓勵的話語，像在廟宇抽到的上上籤一樣，最多四句，不超過50個字。請輸出JSON純文字，格式是{\"comment\":string}，全部合併在同一行就好，我要直接套用到程式裡，請不要有斷行（\\n）等額外字元。"""),
            ],
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
    )

    response = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text

    return json.loads(response)["comment"]
