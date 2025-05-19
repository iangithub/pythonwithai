from openai import OpenAI
import base64

client = OpenAI(
    api_key = "sk-xx",
)

with open('5-3/koko.png', "rb") as image_file:
	base64_str = base64.b64encode(image_file.read()).decode("utf-8")


messages=[
    {
        "role": "user",
        "content": [
            {
				"type": "text", 
			    "text": "請問這兩張圖片是什麼？"
			},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    "detail": "high"
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_str}"
                },
            },
        ],
    }
]

completion = client.chat.completions.create(
    model="gpt-4.1", 
    messages=messages,
)

result = completion.choices[0].message.content

print(result)
