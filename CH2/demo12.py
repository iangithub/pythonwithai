from ollama import chat

model = "llama3.2:3b"

def ai_assistant():
    systemprompt="""
                你是一個熱情、貼心且善解人意的 AI 美食顧問，專門透過親切且具引導性的多輪對話，協助使用者找到最適合他們當下心情和當前天氣的料理。
                你不僅能迅速提供初步的食譜建議，還會透過細心詢問，逐步精確掌握使用者的飲食喜好與需求，並隨時調整你的推薦內容，以提供最適合且具個人化的料理建議。
                當使用者描述自己的情緒或目前所處的天氣狀況時，你會立即提出適合情境的食物選擇，並鼓勵使用者進一步表達更深入的喜好（例如：口味偏好、飲食限制、健康考量等），以持續提升推薦的精準度。
                請務必維持友善、溫暖且富有同理心的語氣，提供具體且易於理解的食譜推薦與烹飪建議，以提升使用者在互動中的滿足感與愉悅感。
                """
    messages = [{"role": "system", "content": systemprompt}]
    while True:
        user_input = input("user => ")
        messages.append({"role": "user", "content": user_input})
        response = chat(model=model, messages=messages)
        assistant_reply = response.message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"assistant => {assistant_reply}")

ai_assistant()
