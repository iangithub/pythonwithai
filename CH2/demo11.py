from ollama import chat

model = "llama3.2:3b"

def language_learning_assistant():
    messages = [{"role": "system", "content": "你是一個語言學習助手，幫助使用者練習對話並提供糾正。"}]
    while True:
        user_input = input("user => ")
        messages.append({"role": "user", "content": user_input})
        response = chat(model=model, messages=messages)
        assistant_reply = response.message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"assistant => {assistant_reply}")

language_learning_assistant()
