from openai import OpenAI

client = OpenAI(
    api_key = "sk-xx",
)    

response = client.images.generate(
    model="dall-e-3",
    prompt="一個可愛的熊熊在森林裡玩耍，陽光透過樹葉灑下來，背景有美麗的花朵和小鳥",
    n=1,
    size="1024x1024",
    quality="hd",
    style="vivid",
)

print("生成的圖片網址：", response.data[0].url)