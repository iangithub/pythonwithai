import requests
from ollama import ChatResponse, chat
model = "llama3.2:3b"

def search_news(query: str) -> str:
    """
    根據指定關鍵字搜尋最新新聞，使用 NewsAPI

    Args:
        query (str): 新聞搜尋關鍵字，支援「科技」、「財經」、「體育」等

    Returns:
        str: 搜尋到的新聞摘要；若查無結果則回傳提示訊息
    """
    # 將中文關鍵字轉換為 NewsAPI 支援的英文分類
    category_map = {
        "科技": "technology",
        "財經": "business",
        "體育": "sports",
        "娛樂": "entertainment",
        "健康": "health",
        "科學": "science",
        "國際": "general"  # NewsAPI 無獨立國際分類，可用 general 表示
    }
    # 若傳入關鍵字未對應，則嘗試用小寫處理
    category = category_map.get(query, query.lower())
    
    # 請將此處的 YOUR_NEWSAPI_KEY 替換成你自己的 API 金鑰
    api_key = "89a3f78febf647dfb7ec2b8f25492e2b"
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "country": "us",  # 取美國新聞
        "language": "en",
        "pageSize": 3,    # 取得前 3 筆新聞
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                return "查無相關新聞。"
            summaries = []
            for article in articles:
                title = article.get("title", "無標題")
                description = article.get("description", "無描述")
                summaries.append(f"標題：{title}\n描述：{description}")
            return "\n\n".join(summaries)
        else:
            return f"API 呼叫失敗，狀態碼：{response.status_code}"
    except Exception as e:
        return f"呼叫 API 時發生錯誤：{str(e)}"

# 定義工具的 schema，讓模型了解工具用途與所需參數格式
search_news_tool = {
    "type": "function",
    "function": {
        "name": "search_news",
        "description": "根據指定關鍵字搜尋最新新聞，回傳新聞摘要",
        "parameters": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "新聞搜尋關鍵字，例如『科技』、『財經』或『體育』"
                }
            }
        }
    }
}

# 建立函式名稱與實際實作對應關係
available_functions = {
    "search_news": search_news,
}

# 模擬使用者輸入訊息，要求搜尋最新的科技新聞
messages = [
    {"role": "system", "content": "你是一位助理，協助整理新聞重點並向我報告。"},
    {"role": "user", "content": "最新的科技新聞。"}
]

print("使用者訊息:", messages)

# 將使用者訊息與工具 schema傳給模型
response: ChatResponse = chat(
    model=model,
    messages=messages,
    tools=[search_news_tool]
)

# 處理模型回傳的工具呼叫結果
if response.message.tool_calls:
    for tool in response.message.tool_calls:
        func_name = tool.function.name
        print("模型呼叫函數:", func_name)
        print("呼叫參數:", tool.function.arguments)
        if (func_to_call := available_functions.get(func_name)):
            try:
                result = func_to_call(**tool.function.arguments)
                print("函數執行結果:", result)
            except Exception as e:
                print("執行函數時發生錯誤:", e)
        else:
            print("找不到對應函數:", func_name)
    
    # 將工具回應加入對話訊息中，再與模型互動以取得最終回覆
    messages.append(response.message)
    messages.append({
        "role": "tool",
        "name": tool.function.name,
        "content": str(result)
    })
    final_response = chat(model, messages=messages)
    print("最終模型回應:", final_response.message.content)
else:
    print("模型未返回任何工具呼叫")
