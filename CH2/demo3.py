from ollama import generate

model = "llama3.2:3b"

# 這是一段未完成的 Python 程式碼，用來爬取網頁內容
prompt = """
import requests
from bs4 import BeautifulSoup

def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
"""

# 指定模型版本與prompt
response = generate(model, prompt)

# 輸出結果
print("模型生成的創作內容：")
print(response.response)

